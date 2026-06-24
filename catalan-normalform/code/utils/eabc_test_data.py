"""
EABC-Test-Daten-Klasse mit persistentem Caching.

Ermöglicht effizienten Zugriff auf vorberechnete EABC-Vektoren und
zugehörige Daten für große Wertebereiche (bis n=10^7).
"""

import h5py
import numpy as np
from pathlib import Path
from typing import Optional, Union, List, Dict, Tuple
import warnings
from tqdm import tqdm

# Importiere Original-Funktionen
import sys
import os
sys.path.append(os.path.dirname(__file__))
from eabc import (
    compute_svn_coordinates,
    compute_eabc_vector,
    compute_H,
    count_prime_factors,
    padicval,
    sum_of_divisors
)


class EABCTestData:
    """
    Ladbare EABC-Test-Daten mit persistentem HDF5-Cache.
    
    Features:
    - Lazy loading: Lade Cache nur bei Bedarf
    - O(1) lookup für vorberechnete Werte
    - Batch-Operationen für Effizienz
    - Fallback auf direkte Berechnung für fehlende Werte
    - Inkrementelles Cache-Update
    
    Usage:
        >>> data = EABCTestData(cache_file="eabc_cache.h5")
        >>> eabc = data.get_eabc(12345)
        >>> H = data.get_concentration(12345)
        >>> coords = data.get_coordinates(12345)
    """
    
    def __init__(
        self,
        cache_file: Optional[Union[str, Path]] = None,
        auto_load: bool = True,
        readonly: bool = True
    ):
        """
        Initialisiert EABC-Test-Daten.
        
        Args:
            cache_file: Pfad zur HDF5-Cache-Datei (optional)
            auto_load: Lade Cache automatisch bei Initialisierung
            readonly: Cache im Read-Only-Modus öffnen (empfohlen für Tests)
        """
        self.cache_file = Path(cache_file) if cache_file else None
        self.readonly = readonly
        self._cache_loaded = False
        self._hdf5_file = None
        
        # Cache-Arrays (Memory-mapped für große Dateien)
        self._n_array = None
        self._omega_array = None
        self._sigma_array = None
        self._v2_array = None
        self._v3_array = None
        self._shell_array = None
        self._e_array = None
        self._a_array = None
        self._b_array = None
        self._c_array = None
        self._omega_eabc_array = None
        self._norm_sq_array = None
        self._H_array = None
        
        # Metadaten
        self.max_n = None
        self.version = None
        
        if auto_load and self.cache_file and self.cache_file.exists():
            self.load_cache()
    
    def __enter__(self):
        """Context manager support."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Schließe HDF5-Datei beim Verlassen des Contexts."""
        self.close()
    
    def close(self):
        """Schließe HDF5-Datei."""
        if self._hdf5_file is not None:
            self._hdf5_file.close()
            self._hdf5_file = None
            self._cache_loaded = False
    
    def load_cache(self):
        """
        Lädt Cache aus HDF5-Datei.
        
        Raises:
            FileNotFoundError: Falls Cache-Datei nicht existiert
        """
        if not self.cache_file.exists():
            raise FileNotFoundError(f"Cache-Datei nicht gefunden: {self.cache_file}")
        
        # Öffne HDF5-Datei
        mode = 'r' if self.readonly else 'r+'
        self._hdf5_file = h5py.File(self.cache_file, mode)
        
        # Lade Metadaten
        if 'metadata' in self._hdf5_file.attrs:
            metadata = self._hdf5_file.attrs['metadata']
            self.max_n = metadata.get('max_n', None)
            self.version = metadata.get('version', None)
        else:
            # Legacy: direkt aus Daten ableiten
            self.max_n = len(self._hdf5_file['data/n'])
            self.version = "unknown"
        
        # Referenziere Datasets (kein vollständiges Laden in Memory)
        data_group = self._hdf5_file['data']
        self._n_array = data_group['n']
        self._omega_array = data_group['omega']
        self._sigma_array = data_group['sigma']
        self._v2_array = data_group['v2']
        self._v3_array = data_group['v3']
        self._shell_array = data_group['shell']
        self._e_array = data_group['e']
        self._a_array = data_group['a']
        self._b_array = data_group['b']
        self._c_array = data_group['c']
        self._omega_eabc_array = data_group['omega_eabc']
        self._norm_sq_array = data_group['norm_sq']
        self._H_array = data_group['H']
        
        self._cache_loaded = True
    
    def _get_index(self, n: int) -> int:
        """
        Berechnet Index für Zahl n im Cache.
        
        Annahme: Cache ist durchgehend von 2 bis max_n.
        Index = n - 2 (da n=2 bei Index 0)
        
        Args:
            n: Natürliche Zahl ≥ 2
            
        Returns:
            Index im Cache-Array
            
        Raises:
            ValueError: Falls n außerhalb des Cache-Bereichs
        """
        if n < 2:
            raise ValueError(f"n muss ≥ 2 sein, erhalten: {n}")
        
        if self.max_n and n > self.max_n:
            raise ValueError(f"n={n} überschreitet Cache-Maximum {self.max_n}")
        
        return n - 2
    
    def _compute_fallback(self, n: int) -> Dict[str, float]:
        """
        Fallback: Berechne direkt, falls nicht im Cache.
        
        Args:
            n: Natürliche Zahl ≥ 2
            
        Returns:
            Dictionary mit allen EABC-Koordinaten
        """
        warnings.warn(
            f"Wert n={n} nicht im Cache, berechne direkt "
            "(Performance-Einbuße!)",
            RuntimeWarning
        )
        coords = compute_svn_coordinates(n)
        # Füge 'shell' hinzu (fehlt in Original-Funktion)
        coords['shell'] = coords['v2'] + coords['v3']
        return coords
    
    def get_coordinates(self, n: int) -> Dict[str, float]:
        """
        Gibt alle EABC-Koordinaten für Zahl n zurück.
        
        Args:
            n: Natürliche Zahl ≥ 2
            
        Returns:
            Dictionary mit Schlüsseln:
            - 'omega': Ω(n)
            - 'sigma': σ(n)
            - 'v2': v₂(n)
            - 'v3': v₃(n)
            - 'shell': S(n) = v₂ + v₃
            - 'e', 'a', 'b', 'c': EABC-Komponenten
            - 'omega_eabc': Ω_EABC = e + a + b + c
            - 'norm_sq': ||v||²
            - 'H': H(n)
        """
        if not self._cache_loaded:
            return self._compute_fallback(n)
        
        try:
            idx = self._get_index(n)
            
            return {
                'n': n,
                'omega': int(self._omega_array[idx]),
                'sigma': int(self._sigma_array[idx]),
                'v2': int(self._v2_array[idx]),
                'v3': int(self._v3_array[idx]),
                'shell': int(self._shell_array[idx]),
                'e': int(self._e_array[idx]),
                'a': int(self._a_array[idx]),
                'b': int(self._b_array[idx]),
                'c': int(self._c_array[idx]),
                'omega_eabc': int(self._omega_eabc_array[idx]),
                'norm_sq': float(self._norm_sq_array[idx]),
                'H': float(self._H_array[idx])
            }
        except (ValueError, IndexError):
            return self._compute_fallback(n)
    
    def get_eabc(self, n: int) -> np.ndarray:
        """
        Gibt EABC-Vektor (e, a, b, c) für Zahl n zurück.
        
        Args:
            n: Natürliche Zahl ≥ 2
            
        Returns:
            numpy array [e, a, b, c]
        """
        coords = self.get_coordinates(n)
        return np.array([coords['e'], coords['a'], coords['b'], coords['c']], dtype=float)
    
    def get_omega(self, n: int) -> int:
        """Gibt Ω(n) - Anzahl Primfaktoren mit Vielfachheit."""
        return self.get_coordinates(n)['omega']
    
    def get_concentration(self, n: int) -> float:
        """Gibt H(n) - Konzentrationsmessung."""
        return self.get_coordinates(n)['H']
    
    def get_shell(self, n: int) -> int:
        """Gibt S(n) = v₂(n) + v₃(n) - Shell-Koordinate."""
        return self.get_coordinates(n)['shell']
    
    def get_sigma(self, n: int) -> int:
        """Gibt σ(n) - Summe der Teiler."""
        return self.get_coordinates(n)['sigma']
    
    def get_coordinates_batch(self, n_values: Union[List[int], np.ndarray]) -> List[Dict[str, float]]:
        """
        Batch-Lookup für mehrere Werte (effizienter als einzeln).
        
        Args:
            n_values: Liste oder Array von Zahlen
            
        Returns:
            Liste von Koordinaten-Dictionaries
        """
        return [self.get_coordinates(n) for n in n_values]
    
    def get_eabc_batch(self, n_values: Union[List[int], np.ndarray]) -> np.ndarray:
        """
        Batch-Lookup für EABC-Vektoren.
        
        Args:
            n_values: Liste oder Array von Zahlen
            
        Returns:
            Array mit Shape (len(n_values), 4) - EABC-Vektoren
        """
        if not self._cache_loaded:
            return np.array([self.get_eabc(n) for n in n_values])
        
        # Effiziente Array-Operation
        n_values = np.asarray(n_values)
        indices = n_values - 2
        
        # Prüfe Gültigkeit
        valid_mask = (indices >= 0) & (indices < len(self._e_array))
        
        result = np.zeros((len(n_values), 4), dtype=float)
        
        # Lade gültige Werte aus Cache
        valid_indices = indices[valid_mask]
        result[valid_mask, 0] = self._e_array[valid_indices]
        result[valid_mask, 1] = self._a_array[valid_indices]
        result[valid_mask, 2] = self._b_array[valid_indices]
        result[valid_mask, 3] = self._c_array[valid_indices]
        
        # Berechne ungültige Werte direkt
        for i in np.where(~valid_mask)[0]:
            result[i] = self.get_eabc(n_values[i])
        
        return result
    
    def get_omega_batch(self, n_values: Union[List[int], np.ndarray]) -> np.ndarray:
        """Batch-Lookup für Ω(n)."""
        if not self._cache_loaded:
            return np.array([self.get_omega(n) for n in n_values])
        
        n_values = np.asarray(n_values)
        indices = n_values - 2
        valid_mask = (indices >= 0) & (indices < len(self._omega_array))
        
        result = np.zeros(len(n_values), dtype=int)
        result[valid_mask] = self._omega_array[indices[valid_mask]]
        
        # Fallback
        for i in np.where(~valid_mask)[0]:
            result[i] = self.get_omega(n_values[i])
        
        return result
    
    def get_concentration_batch(self, n_values: Union[List[int], np.ndarray]) -> np.ndarray:
        """Batch-Lookup für H(n)."""
        if not self._cache_loaded:
            return np.array([self.get_concentration(n) for n in n_values])
        
        n_values = np.asarray(n_values)
        indices = n_values - 2
        valid_mask = (indices >= 0) & (indices < len(self._H_array))
        
        result = np.full(len(n_values), np.nan, dtype=float)
        result[valid_mask] = self._H_array[indices[valid_mask]]
        
        # Fallback
        for i in np.where(~valid_mask)[0]:
            result[i] = self.get_concentration(n_values[i])
        
        return result
    
    def __repr__(self) -> str:
        """String-Repräsentation."""
        if self._cache_loaded:
            return (f"EABCTestData(cache_file={self.cache_file}, "
                   f"max_n={self.max_n:,}, loaded=True)")
        else:
            return f"EABCTestData(cache_file={self.cache_file}, loaded=False)"


def create_cache(
    max_n: int,
    output_file: Union[str, Path],
    chunk_size: int = 100_000,
    show_progress: bool = True,
    compression: str = 'gzip'
) -> None:
    """
    Erstellt EABC-Cache-Datei von n=2 bis n=max_n.
    
    Args:
        max_n: Maximale Zahl (inklusiv)
        output_file: Pfad zur Ausgabe-HDF5-Datei
        chunk_size: Speichere alle X Werte (für Progress & Memory-Effizienz)
        show_progress: Zeige tqdm Progress-Bar
        compression: HDF5-Kompression ('gzip', 'lzf', None)
    """
    output_file = Path(output_file)
    n_values = max_n - 1  # Von 2 bis max_n (inklusiv)
    
    print(f"Erstelle EABC-Cache für n = 2 bis {max_n:,}")
    print(f"Ausgabe: {output_file}")
    print(f"Chunk-Größe: {chunk_size:,}")
    print(f"Kompression: {compression}")
    print()
    
    # Erstelle HDF5-Datei
    with h5py.File(output_file, 'w') as f:
        # Metadaten
        f.attrs['max_n'] = max_n
        f.attrs['version'] = '1.0'
        f.attrs['description'] = 'EABC test data cache'
        
        # Erstelle Datasets
        data_group = f.create_group('data')
        
        # Definiere Chunk-Shape für effizientes Lesen
        chunk_shape = (min(chunk_size, n_values),)
        
        ds_n = data_group.create_dataset(
            'n', shape=(n_values,), dtype='i8',
            chunks=chunk_shape, compression=compression
        )
        ds_omega = data_group.create_dataset(
            'omega', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_sigma = data_group.create_dataset(
            'sigma', shape=(n_values,), dtype='i8',
            chunks=chunk_shape, compression=compression
        )
        ds_v2 = data_group.create_dataset(
            'v2', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_v3 = data_group.create_dataset(
            'v3', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_shell = data_group.create_dataset(
            'shell', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_e = data_group.create_dataset(
            'e', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_a = data_group.create_dataset(
            'a', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_b = data_group.create_dataset(
            'b', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_c = data_group.create_dataset(
            'c', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_omega_eabc = data_group.create_dataset(
            'omega_eabc', shape=(n_values,), dtype='i4',
            chunks=chunk_shape, compression=compression
        )
        ds_norm_sq = data_group.create_dataset(
            'norm_sq', shape=(n_values,), dtype='f8',
            chunks=chunk_shape, compression=compression
        )
        ds_H = data_group.create_dataset(
            'H', shape=(n_values,), dtype='f8',
            chunks=chunk_shape, compression=compression
        )
        
        # Generiere Daten chunk-weise
        iterator = range(2, max_n + 1)
        if show_progress:
            iterator = tqdm(iterator, desc="Generiere Cache", unit="Werte")
        
        # Buffer für Chunk-weise Speicherung
        buffer_n = []
        buffer_omega = []
        buffer_sigma = []
        buffer_v2 = []
        buffer_v3 = []
        buffer_shell = []
        buffer_e = []
        buffer_a = []
        buffer_b = []
        buffer_c = []
        buffer_omega_eabc = []
        buffer_norm_sq = []
        buffer_H = []
        
        write_idx = 0
        
        for n in iterator:
            coords = compute_svn_coordinates(n)
            
            buffer_n.append(n)
            buffer_omega.append(coords['omega'])
            buffer_sigma.append(coords['sigma'])
            buffer_v2.append(coords['v2'])
            buffer_v3.append(coords['v3'])
            buffer_shell.append(coords['v2'] + coords['v3'])
            buffer_e.append(int(coords['e']))
            buffer_a.append(int(coords['a']))
            buffer_b.append(int(coords['b']))
            buffer_c.append(int(coords['c']))
            buffer_omega_eabc.append(int(coords['omega_eabc']))
            buffer_norm_sq.append(coords['norm_sq'])
            buffer_H.append(coords['H'] if not np.isnan(coords['H']) else -1.0)
            
            # Schreibe Chunk, wenn Buffer voll
            if len(buffer_n) >= chunk_size:
                end_idx = write_idx + len(buffer_n)
                
                ds_n[write_idx:end_idx] = buffer_n
                ds_omega[write_idx:end_idx] = buffer_omega
                ds_sigma[write_idx:end_idx] = buffer_sigma
                ds_v2[write_idx:end_idx] = buffer_v2
                ds_v3[write_idx:end_idx] = buffer_v3
                ds_shell[write_idx:end_idx] = buffer_shell
                ds_e[write_idx:end_idx] = buffer_e
                ds_a[write_idx:end_idx] = buffer_a
                ds_b[write_idx:end_idx] = buffer_b
                ds_c[write_idx:end_idx] = buffer_c
                ds_omega_eabc[write_idx:end_idx] = buffer_omega_eabc
                ds_norm_sq[write_idx:end_idx] = buffer_norm_sq
                ds_H[write_idx:end_idx] = buffer_H
                
                write_idx = end_idx
                
                # Leere Buffer
                buffer_n.clear()
                buffer_omega.clear()
                buffer_sigma.clear()
                buffer_v2.clear()
                buffer_v3.clear()
                buffer_shell.clear()
                buffer_e.clear()
                buffer_a.clear()
                buffer_b.clear()
                buffer_c.clear()
                buffer_omega_eabc.clear()
                buffer_norm_sq.clear()
                buffer_H.clear()
        
        # Schreibe letzten Chunk (Rest)
        if buffer_n:
            end_idx = write_idx + len(buffer_n)
            
            ds_n[write_idx:end_idx] = buffer_n
            ds_omega[write_idx:end_idx] = buffer_omega
            ds_sigma[write_idx:end_idx] = buffer_sigma
            ds_v2[write_idx:end_idx] = buffer_v2
            ds_v3[write_idx:end_idx] = buffer_v3
            ds_shell[write_idx:end_idx] = buffer_shell
            ds_e[write_idx:end_idx] = buffer_e
            ds_a[write_idx:end_idx] = buffer_a
            ds_b[write_idx:end_idx] = buffer_b
            ds_c[write_idx:end_idx] = buffer_c
            ds_omega_eabc[write_idx:end_idx] = buffer_omega_eabc
            ds_norm_sq[write_idx:end_idx] = buffer_norm_sq
            ds_H[write_idx:end_idx] = buffer_H
    
    print()
    print(f"✓ Cache erfolgreich erstellt: {output_file}")
    print(f"  Größe: {output_file.stat().st_size / (1024**2):.2f} MB")
