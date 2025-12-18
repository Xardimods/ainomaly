import React, { createContext, useContext, useState, useRef } from 'react';
import { X, AlertTriangle, Info, CheckCircle, HelpCircle } from 'lucide-react';
import { useLanguage } from './LanguageContext';

const DialogContext = createContext();

export const useDialog = () => {
    return useContext(DialogContext);
};

export const DialogProvider = ({ children }) => {
    const { t } = useLanguage();
    const [dialog, setDialog] = useState({
        isOpen: false,
        type: 'confirm', // confirm, alert, prompt
        title: '',
        message: '',
        confirmText: 'OK',
        cancelText: 'Cancel',
        variant: 'default', // default, danger, success, warning
    });

    // We use a ref to store the resolve function of the Promise
    const resolver = useRef(null);

    const closeDialog = (result) => {
        setDialog(prev => ({ ...prev, isOpen: false }));
        if (resolver.current) {
            resolver.current(result);
            resolver.current = null;
        }
    };

    const confirm = (message, options = {}) => {
        return new Promise((resolve) => {
            resolver.current = resolve;
            setDialog({
                isOpen: true,
                type: 'confirm',
                title: options.title || t("dialog.confirm.title") || "Confirmar",
                message,
                confirmText: options.confirmText || t("dialog.confirm.yes") || "Sí",
                cancelText: options.cancelText || t("dialog.confirm.cancel") || "Cancelar",
                variant: options.variant || 'default'
            });
        });
    };

    const alert = (message, options = {}) => {
        return new Promise((resolve) => {
            resolver.current = resolve;
            setDialog({
                isOpen: true,
                type: 'alert',
                title: options.title || t("dialog.alert.title") || "Alerta",
                message,
                confirmText: options.confirmText || "OK",
                variant: options.variant || 'default'
            });
        });
    };

    // Icon mapping based on variant
    const getIcon = () => {
        switch (dialog.variant) {
            case 'danger': return <AlertTriangle className="text-rose-500" size={32} />;
            case 'warning': return <AlertTriangle className="text-amber-500" size={32} />;
            case 'success': return <CheckCircle className="text-emerald-500" size={32} />;
            default: return <HelpCircle className="text-blue-500" size={32} />;
        }
    };

    return (
        <DialogContext.Provider value={{ confirm, alert }}>
            {children}

            {/* Global Dialog Container */}
            {dialog.isOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
                    <div
                        className="bg-white dark:bg-[#1e293b] border border-slate-200 dark:border-white/10 rounded-2xl shadow-2xl max-w-md w-full p-6 transform transition-all scale-100 animate-in zoom-in-95 duration-200 is-dialog"
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="flex gap-4">
                            <div className="flex-shrink-0 pt-1">
                                {getIcon()}
                            </div>
                            <div className="flex-1">
                                <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">
                                    {dialog.title}
                                </h3>
                                <p className="text-slate-600 dark:text-slate-300 text-sm leading-relaxed mb-6">
                                    {dialog.message}
                                </p>

                                <div className="flex justify-end gap-3">
                                    {dialog.type === 'confirm' && (
                                        <button
                                            onClick={() => closeDialog(false)}
                                            className="px-4 py-2 rounded-xl text-sm font-medium text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 transition-colors"
                                        >
                                            {dialog.cancelText}
                                        </button>
                                    )}
                                    <button
                                        onClick={() => closeDialog(true)}
                                        className={`px-6 py-2 rounded-xl text-sm font-medium text-white shadow-lg transition-all transform hover:-translate-y-0.5 ${dialog.variant === 'danger' ? 'bg-rose-500 hover:bg-rose-600 shadow-rose-500/20' :
                                                dialog.variant === 'success' ? 'bg-emerald-500 hover:bg-emerald-600 shadow-emerald-500/20' :
                                                    'bg-blue-600 hover:bg-blue-700 shadow-blue-500/20'
                                            }`}
                                    >
                                        {dialog.confirmText}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </DialogContext.Provider>
    );
};
