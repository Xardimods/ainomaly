import React, { useState } from 'react';
import { Camera, Radio } from 'lucide-react';

const CameraTest = () => {
    const [isStreaming, setIsStreaming] = useState(false);

    return (
        <div className="space-y-6 h-[calc(100vh-8rem)] flex flex-col animate-in fade-in duration-500">
            <header>
                <h2 className="text-3xl font-bold text-white mb-2 tracking-tight">Test de Cámara</h2>
                <p className="text-slate-400">Vista previa en tiempo real y configuración de feeds.</p>
            </header>

            <div className="flex-1 bg-black/40 rounded-2xl border border-white/10 relative overflow-hidden flex items-center justify-center shadow-inner">
                {isStreaming ? (
                    <div className="relative w-full h-full flex items-center justify-center">
                        <div className="text-center z-10">
                            <p className="text-emerald-500 font-mono animate-pulse tracking-widest">[ STREAM ACTIVE ]</p>
                            <p className="text-slate-500 text-sm mt-2">Receiving frames from OpenCV via API...</p>
                        </div>
                        {/* Scanline effect overlay */}
                        <div className="absolute inset-0 bg-[linear-gradient(transparent_50%,rgba(0,0,0,0.25)_50%)] bg-[length:100%_4px] pointer-events-none opacity-50"></div>
                    </div>
                ) : (
                    <div className="text-center text-slate-600">
                        <Camera size={64} className="mx-auto mb-4 opacity-50" />
                        <h3 className="text-xl font-bold mb-2">NO SIGNAL</h3>
                        <p className="text-sm">Feed is currently stopped.</p>
                    </div>
                )}

                {/* Overlay Info */}
                <div className="absolute top-4 right-4 glass-panel px-3 py-1 rounded-lg text-xs font-mono text-emerald-400 border-none bg-black/60">
                    FPS: {isStreaming ? '30' : '0'}
                </div>
            </div>

            <div className="glass-panel p-4 rounded-xl border-white/5 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-slate-400">
                        <Radio size={18} />
                        <span className="text-sm font-medium">Source:</span>
                    </div>
                    <select className="bg-black/20 border border-white/10 rounded-lg px-4 py-2 text-sm outline-none focus:border-blue-500 text-slate-200 transition-colors">
                        <option>Integrated Webcam</option>
                        <option>RTSP Stream 1</option>
                    </select>
                </div>

                <div className="flex gap-3">
                    {!isStreaming ? (
                        <button
                            onClick={() => setIsStreaming(true)}
                            className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-lg font-medium transition-all shadow-lg shadow-blue-900/20 flex items-center gap-2"
                        >
                            <span>▶</span> Iniciar
                        </button>
                    ) : (
                        <button
                            onClick={() => setIsStreaming(false)}
                            className="bg-rose-600 hover:bg-rose-500 text-white px-6 py-2 rounded-lg font-medium transition-all shadow-lg shadow-rose-900/20 flex items-center gap-2"
                        >
                            <span>⏹</span> Detener
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CameraTest;
