import './App.css'
import PitchAnalyzer from './components/PitchAnalyzer'

function App() {
    return (
        <div className="app-container">
            <header className="app-header">
                <h1>Mandarin Pitch Detector</h1>
                <p>Record your voice to analyze the tone</p>
            </header>
            <main>
                <PitchAnalyzer />
            </main>
        </div>
    )
}

export default App
