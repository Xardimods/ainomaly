import React, { useState, useEffect } from 'react';
import { Plus, Camera, Trash2, Maximize2, X, Activity, Power } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useDialog } from '../context/DialogContext';

const CameraFeed = ({ cam }) => {
    // Unique timestamp for this mount instance to force stream refresh
    const [ts] = useState(() => Date.now());

    return (
        <>
            <img
                src={`http://127.0.0.1:8001/video_feed?id=${cam.id}&t=${ts}`}
                alt={cam.name}
                className="w-full h-full object-cover opacity-90 group-hover:opacity-100 transition-opacity bg-black"
                onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
            />
            {/* Fallback if stream fails */}
            <div className="absolute inset-0 hidden items-center justify-center flex-col text-slate-500 bg-slate-200 dark:bg-slate-900/50">
                <Activity size={32} className="mb-2 opacity-50" />
                <span className="text-xs">Connecting...</span>
            </div>
        </>
    );
};

const Cameras = () => {
    const { t } = useLanguage();
    const { confirm } = useDialog();
    const [cameras, setCameras] = useState([]);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [selectedCamera, setSelectedCamera] = useState(null);

    // Form States
    const [camType, setCamType] = useState('rtsp'); // 'webcam' or 'rtsp'
    const [name, setName] = useState('');
    const [webcamIndex, setWebcamIndex] = useState('0');
    // RTSP Fields
    const [ip, setIp] = useState('');
    const [port, setPort] = useState('554');
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [path, setPath] = useState('/stream');

    // Test Status
    const [testStatus, setTestStatus] = useState(null); // 'testing', 'success', 'error', null

    const fetchCameras = () => {
        fetch('http://127.0.0.1:8001/cameras')
            .then(res => res.json())
            .then(data => setCameras(data))
            .catch(console.error);
    };

    useEffect(() => {
        fetchCameras();
        const interval = setInterval(fetchCameras, 5000); // Poll for updates
        return () => clearInterval(interval);
    }, []);

    const handleTestConnection = () => {
        setTestStatus('testing');
        const config = {
            type: camType,
            source: camType === 'webcam' ? webcamIndex : undefined,
            ip, port, user, password, path
        };

        fetch('http://127.0.0.1:8001/cameras/test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        })
            .then(res => res.json())
            .then(data => {
                setTestStatus(data.success ? 'success' : 'error');
            })
            .catch(() => setTestStatus('error'));
    };

    const handleTogglePower = (id, e) => {
        e.stopPropagation();
        fetch(`http://127.0.0.1:8001/cameras/${id}/toggle`, { method: 'POST' })
            .then(() => fetchCameras());
    };

    const handleAddCamera = async () => {
        if (testStatus !== 'success') {
            const confirmed = await confirm("La prueba de conexión no se realizó o falló. ¿Guardar de todos modos?", {
                title: "Conexión Inestable",
                variant: "warning",
                confirmText: "Guardar",
                cancelText: "Revisar"
            });
            if (!confirmed) return;
        }

        const newCamera = {
            name: name || `Camera ${cameras.length + 1}`,
            type: camType,
            source: camType === 'webcam' ? webcamIndex : undefined,
            ip, port, user, password, path
        };

        fetch('http://127.0.0.1:8001/cameras', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCamera)
        })
            .then(res => res.json())
            .then(() => {
                fetchCameras();
                setIsAddModalOpen(false);
                resetForm();
            });
    };

    const resetForm = () => {
        setName('');
        setCamType('rtsp');
        setWebcamIndex('0');
        setIp('');
        setPort('554');
        setUser('');
        setPassword('');
        setPath('/stream');
        setTestStatus(null);
    };

    const handleDeleteCamera = async (id, e) => {
        e.stopPropagation();
        const confirmed = await confirm(t("cam.delete_confirm"), {
            title: t("cam.delete_title") || "Eliminar Cámara",
            variant: "danger",
            confirmText: t("cam.delete_yes") || "Eliminar"
        });
        if (!confirmed) return;

        fetch(`http://127.0.0.1:8001/cameras/${id}`, { method: 'DELETE' })
            .then(() => fetchCameras());
    };

    return (
        <div className="space-y-6 animate-in fade-in duration-500 relative h-full flex flex-col">
            <header className="flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-bold text-slate-900 dark:text-white mb-2 tracking-tight transition-colors">{t("cam.title")}</h2>
                    <p className="text-slate-500 dark:text-slate-400 transition-colors">{t("cam.subtitle")}</p>
                </div>
                <button
                    onClick={() => { resetForm(); setIsAddModalOpen(true); }}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-xl flex items-center gap-2 transition-colors shadow-lg shadow-blue-900/20 hover:-translate-y-0.5"
                >
                    <Plus size={20} />
                    <span>{t("cam.add_camera")}</span>
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 flex-1 overflow-auto p-1">
                {cameras.map((cam) => (
                    <div
                        key={cam.id}
                        onClick={() => cam.enabled && setSelectedCamera(cam)}
                        className={`bg-white dark:bg-white/5 shadow-sm dark:shadow-none rounded-2xl overflow-hidden border border-slate-200 dark:border-white/5 group hover:border-blue-500/50 transition-all cursor-pointer relative aspect-video bg-black ${!cam.enabled ? 'opacity-70' : ''}`}
                    >
                        {cam.enabled ? (
                            <CameraFeed cam={cam} />
                        ) : (
                            <div className="absolute inset-0 flex items-center justify-center flex-col text-slate-500 bg-slate-100 dark:bg-slate-900/80 transition-colors">
                                <Power size={32} className="mb-2 opacity-30" />
                                <span className="text-xs font-mono uppercase tracking-widest opacity-60">OFFLINE</span>
                            </div>
                        )}

                        {/* Overlay Controls */}
                        <div className="absolute top-0 left-0 w-full p-4 bg-gradient-to-b from-black/60 to-transparent flex justify-between items-start opacity-0 group-hover:opacity-100 transition-opacity z-10">
                            <span className="font-medium text-white text-shadow-sm">{cam.name}</span>
                            <div className="flex gap-2">
                                <button
                                    onClick={(e) => handleTogglePower(cam.id, e)}
                                    className={`p-1.5 rounded-lg transition-colors ${cam.enabled ? 'bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500 hover:text-white' : 'bg-slate-700/50 text-slate-200 hover:bg-slate-600 hover:text-white'}`}
                                    title={cam.enabled ? "Apagar" : "Encender"}
                                >
                                    <Power size={16} />
                                </button>
                                <button
                                    onClick={(e) => handleDeleteCamera(cam.id, e)}
                                    className="p-1.5 bg-rose-500/20 text-rose-400 rounded-lg hover:bg-rose-500 hover:text-white transition-colors"
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        </div>

                        {/* Status Light */}
                        {cam.enabled && (
                            <div className="absolute bottom-4 right-4 flex items-center gap-2 px-2 py-1 bg-black/60 rounded-full backdrop-blur-md">
                                <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_#10b981]"></div>
                                <span className="text-[10px] font-mono text-emerald-400">LIVE</span>
                            </div>
                        )}
                    </div>
                ))}

                {cameras.length === 0 && (
                    <div className="col-span-full h-64 flex flex-col items-center justify-center text-slate-500 bg-white dark:bg-white/5 rounded-2xl border-dashed border-2 border-slate-300 dark:border-slate-700 transition-colors">
                        <Camera size={48} className="mb-4 opacity-50" />
                        <p>{t("media.no_files")}</p> {/* Reusing no files msg or specific one available? t("media.no_files") is close enough or use specific */}
                        <button onClick={() => { resetForm(); setIsAddModalOpen(true); }} className="text-blue-500 hover:underline mt-2">{t("cam.add_camera")}</button>
                    </div>
                )}
            </div>

            {/* Add Camera Modal */}
            {isAddModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/80 dark:bg-black/80 backdrop-blur-sm p-4">
                    <div className="bg-white dark:bg-[#0f172a] p-6 rounded-2xl max-w-lg w-full space-y-5 border border-slate-200 dark:border-white/10 shadow-2xl transition-colors">
                        <h3 className="text-xl font-bold text-slate-900 dark:text-white transition-colors">{t("cam.add_camera")}</h3>

                        {/* Type Selection */}
                        <div className="flex gap-4 border-b border-slate-200 dark:border-white/10 pb-4 transition-colors">
                            <button
                                onClick={() => setCamType('rtsp')}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${camType === 'rtsp' ? 'bg-blue-600 text-white' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5'}`}
                            >
                                RTSP / IP
                            </button>
                            <button
                                onClick={() => setCamType('webcam')}
                                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${camType === 'webcam' ? 'bg-blue-600 text-white' : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5'}`}
                            >
                                Webcam USB
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">{t("cam.form.name")}</label>
                                <input
                                    type="text"
                                    className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                    placeholder="Ej: Cámara Principal"
                                    value={name}
                                    onChange={e => setName(e.target.value)}
                                />
                            </div>

                            {camType === 'rtsp' ? (
                                <>
                                    <div className="grid grid-cols-3 gap-4">
                                        <div className="col-span-2 space-y-1">
                                            <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">IP / Host</label>
                                            <input
                                                type="text"
                                                className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                                placeholder="192.168.1.10"
                                                value={ip}
                                                onChange={e => setIp(e.target.value)}
                                            />
                                        </div>
                                        <div className="space-y-1">
                                            <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">Puerto</label>
                                            <input
                                                type="text"
                                                className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                                placeholder="554"
                                                value={port}
                                                onChange={e => setPort(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        <div className="space-y-1">
                                            <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">Usuario</label>
                                            <input
                                                type="text"
                                                className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                                placeholder="admin"
                                                value={user}
                                                onChange={e => setUser(e.target.value)}
                                            />
                                        </div>
                                        <div className="space-y-1">
                                            <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">Contraseña</label>
                                            <input
                                                type="password"
                                                className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                                placeholder="••••••"
                                                value={password}
                                                onChange={e => setPassword(e.target.value)}
                                            />
                                        </div>
                                    </div>

                                    <div className="space-y-1">
                                        <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">Ruta (Stream Path)</label>
                                        <input
                                            type="text"
                                            className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                            placeholder="/Streaming/Channels/101"
                                            value={path}
                                            onChange={e => setPath(e.target.value)}
                                        />
                                    </div>
                                </>
                            ) : (
                                <div className="space-y-1">
                                    <label className="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider transition-colors">{t("cam.form.source")}</label>
                                    <input
                                        type="number"
                                        className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-900 dark:text-white outline-none focus:border-blue-500 transition-colors"
                                        placeholder="0"
                                        value={webcamIndex}
                                        onChange={e => setWebcamIndex(e.target.value)}
                                    />
                                </div>
                            )}
                        </div>

                        {/* Test Actions */}
                        <div className="flex items-center justify-between pt-4 border-t border-slate-200 dark:border-white/10 transition-colors">
                            <div className="flex items-center gap-3">
                                <button
                                    onClick={handleTestConnection}
                                    disabled={testStatus === 'testing'}
                                    className={`text-sm px-4 py-2 rounded-lg border transition-colors ${testStatus === 'success' ? 'text-emerald-500 border-emerald-500/50 bg-emerald-500/10' :
                                        testStatus === 'error' ? 'text-rose-500 border-rose-500/50 bg-rose-500/10' :
                                            'text-slate-500 dark:text-slate-300 border-slate-300 dark:border-white/10 hover:bg-slate-100 dark:hover:bg-white/5'
                                        }`}
                                >
                                    {testStatus === 'testing' ? t("alerts.testing") :
                                        testStatus === 'success' ? '✓ OK' :
                                            testStatus === 'error' ? '✕ Error' :
                                                t("alerts.test")}
                                </button>
                            </div>
                            <div className="flex gap-3">
                                <button onClick={() => setIsAddModalOpen(false)} className="px-4 py-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white transition-colors">{t("cam.form.cancel")}</button>
                                <button onClick={handleAddCamera} className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-500 font-medium shadow-lg shadow-blue-500/20 transition-all">
                                    {t("cam.form.save")}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Expanded Camera Modal */}
            {selectedCamera && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/95 p-4 animate-in zoom-in-95 duration-200">
                    <button
                        onClick={() => setSelectedCamera(null)}
                        className="absolute top-4 right-4 text-white/50 hover:text-white z-50 bg-black/20 p-2 rounded-full transition-colors"
                    >
                        <X size={24} />
                    </button>
                    <div className="w-full h-full max-w-7xl max-h-[90vh] flex flex-col">
                        <div className="flex-1 bg-black rounded-2xl overflow-hidden relative border border-white/10">
                            <img
                                src={`http://127.0.0.1:8001/video_feed?id=${selectedCamera.id}`}
                                className="w-full h-full object-contain"
                            />
                            <div className="absolute top-4 left-4 text-white font-mono bg-black/50 px-3 py-1 rounded">
                                {selectedCamera.name}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Cameras;
