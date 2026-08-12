import React, { useState } from "react";
import "./App.css";

function App() {
    const [open, setOpen] = useState(false);

    return (
        <div className="deskpilot">

            {/* Floating DeskPilot Robot */}
            <div
                className="avatar"
                onClick={() => setOpen(!open)}
                title="Open DeskPilot"
            >
                <div className="robot">🤖</div>

                <div className="name">
                    DeskPilot
                </div>
            </div>

            {/* Assistant Panel */}
            {open && (
                <div className="assistant-panel">

                    {/* Header */}
                    <div className="panel-header">
                        <span>🤖 DeskPilot</span>

                        <button
                            className="close-button"
                            onClick={() => setOpen(false)}
                        >
                            ×
                        </button>
                    </div>

                    {/* Message */}
                    <div className="panel-message">

                        <div className="small-robot">
                            🤖
                        </div>

                        <div>
                            <strong>Hello!</strong>
                            <br />
                            How can I help you?
                        </div>

                    </div>

                    {/* Voice Area */}
                    <div className="voice-area">

                        <button className="mic-button">
                            🎤
                        </button>

                        <p>
                            Click the microphone and speak
                        </p>

                    </div>

                </div>
            )}

        </div>
    );
}

export default App;