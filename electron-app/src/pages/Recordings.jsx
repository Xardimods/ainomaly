import React, { useState, useEffect } from 'react';
import { Play, FileVideo, Download, Trash2 } from 'lucide-react';

const Recordings = () => {
    const [recordings, setRecordings] = useState([]);

    useEffect(() => {
        // Fetch recordings from Python backend
        fetch('http://127.0.0.1:8001/recordings')
            .then(res => res.json())
            .then(data => setRecordings(data))
            .catch(err => console.error("Failed to fetch recordings", err));
    }, []);

    const [selectedVideo, setSelectedVideo] = useState(null);

    return (
        <div className="space-y-6 animate-in fade-in duration-500 relative">
            {/* Video Modal */}
            {selectedVideo && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
                    <div className="bg-slate-900 rounded-2xl border border-white/10 w-full max-w-4xl overflow-hidden shadow-2xl relative">
                        <div className="p-4 border-b border-white/5 flex justify-between items-center bg-black/20">
                            <h3 className="font-medium text-white">{selectedVideo}</h3>
                            <button
                                onClick={() => setSelectedVideo(null)}
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                ✕
                            </button>
                        </div>
                        <div className="aspect-video bg-black relative">
                            <video
                                src={`http://127.0.0.1:8001/recordings_files/${selectedVideo}`}
                                controls
                                autoPlay
                                className="w-full h-full"
                            />
                        </div>
                    </div>
                </div>
            )}

            <header>
                <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Grabaciones</h2>
                <p className="text-slate-400">Gestiona el historial de grabaciones de seguridad.</p>
            </header>

            <div className="glass-panel rounded-2xl overflow-hidden border-white/5">
                <table className="w-full text-left">
                    <thead>
                        <tr className="bg-white/5 text-slate-400 text-sm">
                            <th className="p-4 font-medium">Nombre</th>
                            <th className="p-4 font-medium">Fecha</th>
                            <th className="p-4 font-medium">Tamaño</th>
                            <th className="p-4 font-medium text-right">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {recordings.length > 0 ? (
                            recordings.map((rec) => (
                                <tr key={rec.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                                    <td className="p-4 flex items-center gap-3">
                                        <div className="p-2 bg-indigo-500/20 rounded-lg text-indigo-400">
                                            <FileVideo size={20} />
                                        </div>
                                        <span className="font-medium text-slate-200">{rec.name}</span>
                                    </td>
                                    <td className="p-4 text-slate-400">{rec.date}</td>
                                    <td className="p-4 text-slate-400">25 MB</td>
                                    <td className="p-4 text-right">
                                        <div className="flex justify-end gap-2">
                                            <button
                                                onClick={() => setSelectedVideo(rec.name)}
                                                className="p-2 hover:bg-emerald-500/20 rounded-lg text-emerald-400 transition-colors"
                                                title="Reproducir"
                                            >
                                                <Play size={18} />
                                            </button>
                                            <button className="p-2 hover:bg-blue-500/20 rounded-lg text-blue-400 transition-colors" title="Descargar">
                                                <Download size={18} />
                                            </button>
                                            <button className="p-2 hover:bg-rose-500/20 rounded-lg text-rose-400 transition-colors" title="Eliminar">
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))
                        ) : (
                            <tr>
                                <td colSpan={4} className="p-12 text-center text-slate-500">
                                    No se encontraron grabaciones.
                                </td>
                            </tr>
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Recordings;
