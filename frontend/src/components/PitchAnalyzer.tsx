import React, { useState } from 'react';
import { useReactMediaRecorder } from 'react-media-recorder';
import axios from 'axios';
import { Mic, Square, Loader2, AlertCircle } from 'lucide-react';
import { convertBlobToWav } from '../utils/audioHelpers';

interface AnalysisResult {
    tone: string;
    slope: number;
    is_dipping: boolean;
    plot_image: string;
}

const PitchAnalyzer: React.FC = () => {
    const [result, setResult] = useState<AnalysisResult | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const { status, startRecording, stopRecording, mediaBlobUrl } =
        useReactMediaRecorder({ audio: true });

    const handleAnalyze = async () => {
        if (!mediaBlobUrl) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const blob = await fetch(mediaBlobUrl).then((r) => r.blob());
            // Enforce WAV conversion using the helper function
            const file = await convertBlobToWav(blob);

            const formData = new FormData();
            formData.append('audio', file);

            const response = await axios.post('http://127.0.0.1:8000/analyze_tone_praat', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setResult(response.data);
        } catch (err: any) {
            console.error(err);
            setError(err.response?.data?.detail || 'An error occurred during analysis');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="pitch-analyzer">
            <div className="controls">
                {status !== 'recording' ? (
                    <button className="btn btn-primary" onClick={startRecording}>
                        <Mic size={20} /> Start Recording
                    </button>
                ) : (
                    <button className="btn btn-danger" onClick={stopRecording}>
                        <Square size={20} /> Stop Recording
                    </button>
                )}

                {mediaBlobUrl && (
                    <button
                        className="btn btn-secondary"
                        onClick={handleAnalyze}
                        disabled={loading || status === 'recording'}
                    >
                        {loading ? <Loader2 className="spin" size={20} /> : 'Analyze Pitch'}
                    </button>
                )}
            </div>

            {status === 'recording' && <div className="recording-indicator">Recording...</div>}

            {mediaBlobUrl && (
                <div className="audio-preview">
                    <audio src={mediaBlobUrl} controls />
                </div>
            )}

            {error && (
                <div className="error-message">
                    <AlertCircle size={20} />
                    <span>{error}</span>
                </div>
            )}

            {result && (
                <div className="result-container">
                    <div className="result-card">
                        <h3>Analysis Result</h3>
                        <div className="result-item">
                            <span className="label">Tone:</span>
                            <span className="value">{result.tone}</span>
                        </div>
                        <div className="result-item">
                            <span className="label">Slope:</span>
                            <span className="value">{result.slope.toFixed(4)}</span>
                        </div>
                        <div className="result-item">
                            <span className="label">Dipping:</span>
                            <span className="value">{result.is_dipping ? 'Yes' : 'No'}</span>
                        </div>
                    </div>

                    {result.plot_image && (
                        <div className="plot-container">
                            <img
                                src={`data:image/png;base64,${result.plot_image}`}
                                alt="Pitch Contour Plot"
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default PitchAnalyzer;
