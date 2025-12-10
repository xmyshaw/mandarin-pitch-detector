import toWav from 'audiobuffer-to-wav';

export const convertBlobToWav = async (blob: Blob): Promise<File> => {
    const arrayBuffer = await blob.arrayBuffer();
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const wavBuffer = toWav(audioBuffer);
    const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });
    return new File([wavBlob], 'recording.wav', { type: 'audio/wav' });
};
