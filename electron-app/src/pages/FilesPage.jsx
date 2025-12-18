import React, { useState, useEffect } from 'react';
import { Image, Trash2, Download, Search, Calendar, FileText, X } from 'lucide-react';

const FilesPage = () => {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedImage, setSelectedImage] = useState(null);
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetch('http://127.0.0.1:8001/snapshots')
            .then(res => res.json())
            .then(data => {
                setFiles(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, []);

    const handleDelete = (filename, e) => {
        if (e) e.stopPropagation();
        if (!confirm("¿Estás seguro de eliminar este archivo?")) return;

        // If the file is currently open in the modal, close it first to avoid locks
        if (selectedImage?.name === filename) {
            setSelectedImage(null);
        }

        fetch(`http://127.0.0.1:8001/api/snapshots/${filename}`, { method: 'DELETE' })
            .then(async res => {
                if (res.ok) return { status: 'deleted' };
                try {
                    return await res.json();
                } catch {
                    return { error: `HTTP ${res.status} ${res.statusText}` };
                }
            })
            .then(data => {
                if (data.status === 'deleted') {
                    setFiles(prev => prev.filter(f => f.name !== filename));
                } else {
                    const msg = data.error || data.detail || "Error desconocido";
                    alert("Error eliminando: " + msg);
                }
            })
            .catch(err => {
                console.error("Error deleting:", err);
                alert("Error de conexión al eliminar.");
            });
    };

    const handleDownload = (file, e) => {
        e.stopPropagation();
        const link = document.createElement("a");
        link.href = `http://127.0.0.1:8001${file.url}`;
        link.download = file.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const filteredFiles = files.filter(f =>
        f.name.toLowerCase().includes(search.toLowerCase()) ||
        f.date.includes(search)
    );

    return (
        <div className="space-y-6 animate-in fade-in duration-500 max-w-7xl mx-auto h-full flex flex-col">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Galería de Archivos</h2>
                    <p className="text-slate-400">Snapshots y capturas de alertas de seguridad.</p>
                </div>

                <div className="flex gap-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <input
                            type="text"
                            placeholder="Buscar por fecha..."
                            value={search}
                            onChange={e => setSearch(e.target.value)}
                            className="bg-black/20 border border-white/10 rounded-xl pl-10 pr-4 py-2 text-white focus:outline-none focus:border-blue-500 w-64 text-sm"
                        />
                    </div>
                </div>
            </header>

            {loading ? (
                <div className="flex-1 flex items-center justify-center">
                    <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
            ) : (
                <div className="flex-1 overflow-y-auto pr-2">
                    {filteredFiles.length > 0 ? (
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                            {filteredFiles.map((file, idx) => (
                                <div
                                    key={idx}
                                    onClick={() => setSelectedImage(file)}
                                    className="group relative aspect-video bg-black/40 rounded-xl overflow-hidden border border-white/5 hover:border-blue-500/50 transition-all cursor-pointer"
                                >
                                    <img
                                        src={`http://127.0.0.1:8001${file.url}`}
                                        alt={file.name}
                                        className="w-full h-full object-cover opacity-80 group-hover:opacity-100 group-hover:scale-105 transition-all duration-500"
                                    />

                                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-3">
                                        <p className="text-white text-xs font-medium truncate">{file.name}</p>
                                        <p className="text-slate-400 text-[10px]">{file.date} • {file.size}</p>

                                        <div className="flex gap-2 mt-2 justify-end">
                                            <button
                                                onClick={(e) => handleDownload(file, e)}
                                                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
                                                title="Descargar"
                                            >
                                                <Download size={14} />
                                            </button>
                                            <button
                                                onClick={(e) => handleDelete(file.name, e)}
                                                className="p-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/40 text-rose-400 transition-colors"
                                                title="Eliminar"
                                            >
                                                <Trash2 size={14} />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="h-64 flex flex-col items-center justify-center text-slate-500 border-2 border-dashed border-white/5 rounded-2xl">
                            <Image size={48} className="mb-4 opacity-50" />
                            <p>No se encontraron archivos.</p>
                        </div>
                    )}
                </div>
            )}

            {/* Lightbox Modal */}
            {selectedImage && (
                <div
                    className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200"
                    onClick={() => setSelectedImage(null)}
                >
                    <button
                        className="absolute top-4 right-4 text-white/50 hover:text-white p-2 rounded-full hover:bg-white/10 transition-colors"
                        onClick={() => setSelectedImage(null)}
                    >
                        <X size={32} />
                    </button>

                    <div className="max-w-5xl max-h-[90vh] w-full flex flex-col gap-4" onClick={e => e.stopPropagation()}>
                        <div className="relative rounded-2xl overflow-hidden border border-white/10 shadow-2xl bg-black">
                            <img
                                src={`http://127.0.0.1:8001${selectedImage.url}`}
                                alt={selectedImage.name}
                                className="w-full h-full object-contain max-h-[80vh]"
                            />
                        </div>

                        <div className="flex justify-between items-center px-2">
                            <div>
                                <h3 className="text-white font-medium">{selectedImage.name}</h3>
                                <p className="text-slate-400 text-sm">{selectedImage.date} • {selectedImage.size}</p>
                            </div>
                            <div className="flex gap-3">
                                <button
                                    onClick={(e) => handleDownload(selectedImage, e)}
                                    className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg transition-colors"
                                >
                                    <Download size={18} /> Descargar
                                </button>
                                <button
                                    onClick={(e) => {
                                        handleDelete(selectedImage.name, e);
                                    }}
                                    className="flex items-center gap-2 px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 rounded-lg transition-colors border border-rose-500/20"
                                >
                                    <Trash2 size={18} /> Eliminar
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default FilesPage;
