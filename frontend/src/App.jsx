// // import React, { useState } from "react";
// // import "./App.css";

// // function App() {
// //     const [open, setOpen] = useState(false);

// //     return (
// //         <div className="deskpilot">

// //             {/* Floating DeskPilot Robot */}
// //             <div
// //                 className="avatar"
// //                 onClick={() => setOpen(!open)}
// //                 title="Open DeskPilot"
// //             >
// //                 <div className="robot">🤖</div>

// //                 <div className="name">
// //                     DeskPilot
// //                 </div>
// //             </div>

// //             {/* Assistant Panel */}
// //             {open && (
// //                 <div className="assistant-panel">

// //                     {/* Header */}
// //                     <div className="panel-header">
// //                         <span>🤖 DeskPilot</span>

// //                         <button
// //                             className="close-button"
// //                             onClick={() => setOpen(false)}
// //                         >
// //                             ×
// //                         </button>
// //                     </div>

// //                     {/* Message */}
// //                     <div className="panel-message">

// //                         <div className="small-robot">
// //                             🤖
// //                         </div>

// //                         <div>
// //                             <strong>Hello!</strong>
// //                             <br />
// //                             How can I help you?
// //                         </div>

// //                     </div>

// //                     {/* Voice Area */}
// //                     <div className="voice-area">

// //                         <button className="mic-button">
// //                             🎤
// //                         </button>

// //                         <p>
// //                             Click the microphone and speak
// //                         </p>

// //                     </div>

// //                 </div>
// //             )}

// //         </div>
// //     );
// // }

// // export default App;
// import React, { useState, useEffect, useRef } from "react";
// import "./App.css";

// function App() {
//     const [open, setOpen] = useState(false);
//     const [listening, setListening] = useState(false);
//     const [transcript, setTranscript] = useState("");
//     const [response, setResponse] = useState("");
//     const [status, setStatus] = useState("Ready");

//     const recognitionRef = useRef(null);

//     useEffect(() => {
//         const SpeechRecognition =
//             window.SpeechRecognition ||
//             window.webkitSpeechRecognition;

//         if (!SpeechRecognition) {
//             setStatus("Voice recognition not supported");
//             return;
//         }

//         const recognition = new SpeechRecognition();

//         recognition.continuous = true;
//         recognition.interimResults = true;
//         recognition.lang = "en-US";

//         recognition.onstart = () => {
//             setListening(true);
//             setStatus("Listening...");
//         };

//         recognition.onresult = (event) => {
//             let finalText = "";
//             let interimText = "";

//             for (
//                 let i = event.resultIndex;
//                 i < event.results.length;
//                 i++
//             ) {
//                 const text = event.results[i][0].transcript;

//                 if (event.results[i].isFinal) {
//                     finalText += text;
//                 } else {
//                     interimText += text;
//                 }
//             }

//             if (finalText) {
//                 setTranscript(finalText);
//                 sendCommand(finalText);
//             } else {
//                 setTranscript(interimText);
//             }
//         };

//         recognition.onerror = (event) => {
//             console.log("Speech recognition error:", event.error);

//             if (event.error === "not-allowed") {
//                 setStatus("Microphone permission denied");
//             } else {
//                 setStatus("Voice error");
//             }

//             setListening(false);
//         };

//         recognition.onend = () => {
//             /*
//              * Automatically restart while the user
//              * still wants to speak.
//              */
//             if (recognitionRef.current?._shouldListen) {
//                 try {
//                     recognition.start();
//                 } catch (error) {
//                     console.log("Restart error:", error);
//                 }
//             } else {
//                 setListening(false);
//                 setStatus("Ready");
//             }
//         };

//         recognitionRef.current = recognition;

//         return () => {
//             recognition._shouldListen = false;
//             recognition.stop();
//         };
//     }, []);

//     const startListening = () => {
//         const recognition = recognitionRef.current;

//         if (!recognition) {
//             alert("Speech recognition is not supported.");
//             return;
//         }

//         recognition._shouldListen = true;

//         try {
//             recognition.start();
//         } catch (error) {
//             console.log("Already listening");
//         }
//     };

//     const stopListening = () => {
//         const recognition = recognitionRef.current;

//         if (!recognition) return;

//         recognition._shouldListen = false;
//         recognition.stop();

//         setListening(false);
//         setStatus("Ready");
//     };

//     const toggleListening = () => {
//         if (listening) {
//             stopListening();
//         } else {
//             startListening();
//         }
//     };

//     const sendCommand = async (command) => {
//         if (!command.trim()) return;

//         setStatus("DeskPilot is thinking...");
//         setResponse("");

//         try {
//             const res = await fetch("http://127.0.0.1:8000/api/command", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json",
//                 },
//                 body: JSON.stringify({
//                     command: command,
//                 }),
//             });

//             const data = await res.json();

//             if (!res.ok) {
//                 throw new Error(data.detail || "Command failed");
//             }

//             console.log("Backend response:", data);

//             setResponse(
//                 typeof data.response === "string"
//                     ? data.response
//                     : JSON.stringify(data.response)
//             );

//             setStatus("Command completed");
//         } catch (error) {
//             console.error(error);

//             setResponse(
//                 "I couldn't connect to the DeskPilot backend."
//             );

//             setStatus("Backend connection failed");
//         }
//     };

//     return (
//         <div className="deskpilot">

//             {/* Floating Avatar */}
//             <div
//                 className="avatar"
//                 onClick={() => setOpen(!open)}
//                 title="Open DeskPilot"
//             >
//                 <div className="robot">
//                     🤖
//                 </div>

//                 <div className="name">
//                     DeskPilot
//                 </div>
//             </div>

//             {/* Assistant Panel */}
//             {open && (
//                 <div className="assistant-panel">

//                     {/* Header */}
//                     <div className="panel-header">

//                         <span>
//                             🤖 DeskPilot
//                         </span>

//                         <button
//                             className="close-button"
//                             onClick={() => setOpen(false)}
//                         >
//                             ×
//                         </button>

//                     </div>

//                     {/* Greeting */}
//                     <div className="panel-message">

//                         <div className="small-robot">
//                             🤖
//                         </div>

//                         <div>
//                             <strong>Hello!</strong>
//                             <br />
//                             Tell me what you want me to do.
//                         </div>

//                     </div>

//                     {/* Status */}
//                     <div className="status">
//                         {status}
//                     </div>

//                     {/* Transcript */}
//                     {transcript && (
//                         <div className="transcript">
//                             <strong>You:</strong>
//                             <br />
//                             {transcript}
//                         </div>
//                     )}

//                     {/* Response */}
//                     {response && (
//                         <div className="assistant-response">
//                             <strong>DeskPilot:</strong>
//                             <br />
//                             {response}
//                         </div>
//                     )}

//                     {/* Voice Area */}
//                     <div className="voice-area">

//                         <button
//                             className={`mic-button ${
//                                 listening ? "listening" : ""
//                             }`}
//                             onClick={toggleListening}
//                         >
//                             {listening ? "⏹️" : "🎤"}
//                         </button>

//                         <p>
//                             {listening
//                                 ? "Listening... Click to stop"
//                                 : "Click the microphone and speak"}
//                         </p>

//                     </div>

//                 </div>
//             )}

//         </div>
//     );
// }

// export default App;
// import React, { useState, useRef } from "react";
// import "./App.css";

// function App() {
//     const [open, setOpen] = useState(false);
//     const [listening, setListening] = useState(false);
//     const [command, setCommand] = useState("");
//     const [response, setResponse] = useState("");
//     const [processing, setProcessing] = useState(false);

//     const recognitionRef = useRef(null);

//     // ==========================================
//     // SEND COMMAND TO DESKPILOT BACKEND
//     // ==========================================

//     const sendCommandToBackend = async (text) => {
//         if (!text.trim()) return;

//         setProcessing(true);
//         setResponse("DeskPilot is working...");

//         try {
//             const result = await fetch(
//                 "http://127.0.0.1:8000/api/command",
//                 {
//                     method: "POST",

//                     headers: {
//                         "Content-Type": "application/json",
//                         "Accept": "application/json",
//                     },

//                     body: JSON.stringify({
//                         command: text,
//                     }),
//                 }
//             );

//             if (!result.ok) {
//                 throw new Error(
//                     `Backend returned ${result.status}`
//                 );
//             }

//             const data = await result.json();

//             console.log("DeskPilot backend response:", data);

//             setResponse(
//                 data.response ||
//                 "Command completed."
//             );

//         } catch (error) {
//             console.error("DeskPilot error:", error);

//             setResponse(
//                 "❌ Could not connect to DeskPilot backend."
//             );
//         }

//         setProcessing(false);
//     };


//     // ==========================================
//     // START VOICE RECOGNITION
//     // ==========================================

//     const startListening = () => {

//         // Browser compatibility
//         const SpeechRecognition =
//             window.SpeechRecognition ||
//             window.webkitSpeechRecognition;

//         if (!SpeechRecognition) {
//             alert(
//                 "Speech recognition is not supported in this browser. Please use Google Chrome."
//             );
//             return;
//         }

//         // Already listening
//         if (listening) {
//             recognitionRef.current?.stop();
//             return;
//         }

//         const recognition = new SpeechRecognition();

//         recognition.lang = "en-US";

//         recognition.continuous = false;

//         recognition.interimResults = false;

//         recognition.maxAlternatives = 1;

//         recognitionRef.current = recognition;


//         // ==========================================
//         // SPEECH START
//         // ==========================================

//         recognition.onstart = () => {
//             console.log("🎤 DeskPilot listening...");

//             setListening(true);

//             setCommand("");

//             setResponse("Listening...");
//         };


//         // ==========================================
//         // SPEECH RESULT
//         // ==========================================

//         recognition.onresult = (event) => {

//             const transcript =
//                 event.results[0][0].transcript;

//             console.log(
//                 "🎤 User said:",
//                 transcript
//             );

//             setCommand(transcript);

//             setResponse(
//                 `You said: "${transcript}"`
//             );

//             // Send voice command to backend
//             sendCommandToBackend(transcript);
//         };


//         // ==========================================
//         // SPEECH END
//         // ==========================================

//         recognition.onend = () => {

//             console.log(
//                 "🎤 DeskPilot stopped listening."
//             );

//             setListening(false);
//         };


//         // ==========================================
//         // SPEECH ERROR
//         // ==========================================

//         recognition.onerror = (event) => {

//             console.error(
//                 "Speech recognition error:",
//                 event.error
//             );

//             setListening(false);

//             if (event.error === "not-allowed") {
//                 setResponse(
//                     "❌ Microphone permission was denied."
//                 );
//             } else {
//                 setResponse(
//                     `❌ Voice error: ${event.error}`
//                 );
//             }
//         };


//         recognition.start();
//     };


//     // ==========================================
//     // UI
//     // ==========================================

//     return (
//         <div className="deskpilot">

//             {/* =================================
//                 FLOATING DESKPILOT AVATAR
//             ================================= */}

//             <div
//                 className="avatar"
//                 onClick={() => setOpen(!open)}
//                 title="Open DeskPilot"
//             >

//                 <div className="robot">

//                     {/* Antenna */}
//                     <div className="antenna">
//                         <div className="antenna-light"></div>
//                     </div>


//                     {/* Head */}
//                     <div className="robot-head">

//                         <div className="robot-ear left-ear"></div>

//                         <div className="robot-ear right-ear"></div>


//                         <div className="robot-face">

//                             <div className="eye left-eye"></div>

//                             <div className="eye right-eye"></div>

//                             <div className="robot-mouth"></div>

//                         </div>

//                     </div>


//                     {/* Body */}
//                     <div className="robot-body">

//                         <div className="chest-light">
//                             D
//                         </div>

//                     </div>

//                 </div>


//                 <div className="name">
//                     DeskPilot
//                 </div>

//             </div>


//             {/* =================================
//                 ASSISTANT PANEL
//             ================================= */}

//             {open && (

//                 <div
//                     className="assistant-panel"
//                     onClick={(e) => e.stopPropagation()}
//                 >

//                     {/* Header */}

//                     <div className="panel-header">

//                         <div className="header-title">

//                             <div className="mini-logo">
//                                 D
//                             </div>

//                             <span>
//                                 DeskPilot
//                             </span>

//                         </div>


//                         <button
//                             className="close-button"
//                             onClick={() => setOpen(false)}
//                         >
//                             ×
//                         </button>

//                     </div>


//                     {/* Greeting */}

//                     <div className="panel-message">

//                         <div className="mini-robot">

//                             <div className="mini-face">

//                                 <div className="mini-eye"></div>

//                                 <div className="mini-eye"></div>

//                             </div>

//                         </div>


//                         <div className="message-text">

//                             <strong>
//                                 Hello! 👋
//                             </strong>

//                             <br />

//                             How can I help you?

//                         </div>

//                     </div>


//                     {/* =================================
//                         COMMAND DISPLAY
//                     ================================= */}

//                     {command && (

//                         <div className="command-box">

//                             <div className="command-label">
//                                 Your command
//                             </div>

//                             <div className="command-text">
//                                 {command}
//                             </div>

//                         </div>

//                     )}


//                     {/* =================================
//                         RESPONSE
//                     ================================= */}

//                     {response && (

//                         <div className="response-box">

//                             <div className="response-label">
//                                 DeskPilot
//                             </div>

//                             <div className="response-text">
//                                 {response}
//                             </div>

//                         </div>

//                     )}


//                     {/* =================================
//                         VOICE AREA
//                     ================================= */}

//                     <div className="voice-area">

//                         <button
//                             className={`mic-button ${
//                                 listening
//                                     ? "listening"
//                                     : ""
//                             } ${
//                                 processing
//                                     ? "processing"
//                                     : ""
//                             }`}
//                             onClick={startListening}
//                             disabled={processing}
//                         >

//                             {listening
//                                 ? "⏹️"
//                                 : "🎤"}

//                         </button>


//                         <p>

//                             {processing
//                                 ? "DeskPilot is working..."
//                                 : listening
//                                 ? "Listening..."
//                                 : "Click the microphone and speak"}

//                         </p>

//                     </div>

//                 </div>

//             )}

//         </div>
//     );
// }

// export default App;
import React, { useState, useRef } from "react";
import "./App.css";

function App() {
  const [open, setOpen] = useState(false);
  const [recording, setRecording] = useState(false);

  const [status, setStatus] = useState(
    "Click the robot and speak"
  );

  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");

  const [avatarState, setAvatarState] = useState("idle");

  // =========================================================
  // EMAIL CONFIRMATION STATE
  // =========================================================

  const [pendingEmail, setPendingEmail] = useState(null);
  const [emailActionLoading, setEmailActionLoading] =
    useState(false);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // =========================================================
  // SPEAK DESKPILOT RESPONSE
  // =========================================================

  const speakResponse = (text) => {
  if (!text || !("speechSynthesis" in window)) {
    return;
  }

  window.speechSynthesis.cancel();

  const utterance =
    new SpeechSynthesisUtterance(text);

  utterance.rate = 1;
  utterance.pitch = 1;
  utterance.volume = 1;

  const voices =
    window.speechSynthesis.getVoices();

  const femaleVoice = voices.find((voice) =>
    /female|zira|samantha|aria|jenny|sara/i.test(voice.name) &&
    voice.lang.startsWith("en")
  );

  if (femaleVoice) {
    utterance.voice = femaleVoice;
  }

  utterance.onstart = () => {
    setAvatarState("speaking");
    setStatus("DeskPilot is speaking...");
  };

  utterance.onend = () => {
    setAvatarState("completed");
    setStatus("Command completed");

    setTimeout(() => {
      setAvatarState("idle");
    }, 1500);
  };

  utterance.onerror = () => {
    setAvatarState("completed");
    setStatus("Command completed");

    setTimeout(() => {
      setAvatarState("idle");
    }, 1500);
  };

  window.speechSynthesis.speak(utterance);
};

  // =========================================================
  // CHECK FOR EMAIL CONFIRMATION
  // =========================================================

  const checkForEmailConfirmation = (data) => {
    if (
      data?.response &&
      typeof data.response === "object" &&
      data.response.status === "pending_confirmation"
    ) {
      setPendingEmail(data.response);

      return true;
    }

    return false;
  };

  // =========================================================
  // START RECORDING
  // =========================================================

  const startRecording = async () => {
    try {
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }

      const stream =
        await navigator.mediaDevices.getUserMedia({
          audio: true,
        });

      const recorder =
        new MediaRecorder(stream);

      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(
            event.data
          );
        }
      };

      recorder.onstop = async () => {
        stream
          .getTracks()
          .forEach((track) => track.stop());

        const audioBlob = new Blob(
          audioChunksRef.current,
          {
            type: "audio/webm",
          }
        );

        await sendVoiceCommand(audioBlob);
      };

      recorder.start();

      setRecording(true);
      setAvatarState("listening");

      setStatus("Listening...");
      setTranscript("");
      setResponse("");

    } catch (error) {
      console.error(
        "Microphone error:",
        error
      );

      setRecording(false);
      setAvatarState("error");

      setStatus(
        "Microphone permission denied"
      );
    }
  };

  // =========================================================
  // STOP RECORDING
  // =========================================================

  const stopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state !==
        "inactive"
    ) {
      mediaRecorderRef.current.stop();

      setRecording(false);

      setAvatarState("thinking");

      setStatus(
        "DeskPilot is thinking..."
      );
    }
  };

  // =========================================================
  // SEND VOICE COMMAND
  // =========================================================

  const sendVoiceCommand = async (
    audioBlob
  ) => {
    try {
      setAvatarState("thinking");

      setStatus(
        "DeskPilot is thinking..."
      );

      const formData = new FormData();

      formData.append(
        "audio",
        audioBlob,
        "deskpilot-command.webm"
      );

      const res = await fetch(
        "http://127.0.0.1:8000/api/voice",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.detail ||
            "Voice command failed"
        );
      }

      setTranscript(
        data.transcript || ""
      );

      // =====================================================
      // EMAIL CONFIRMATION
      // =====================================================

      const confirmationRequired =
        checkForEmailConfirmation(data);

      if (confirmationRequired) {
        const confirmationMessage =
          "The email is ready. Please review it and confirm before sending.";

        setResponse(
          confirmationMessage
        );

        setAvatarState("completed");

        setStatus(
          "Waiting for your confirmation"
        );

        speakResponse(
          confirmationMessage
        );

        return;
      }

      // =====================================================
      // NORMAL RESPONSE
      // =====================================================

      const spokenResponse =
        typeof data.response ===
        "string"
          ? data.response
          : JSON.stringify(
              data.response
            );

      setResponse(
        spokenResponse
      );

      setAvatarState("completed");

      setStatus(
        "Command completed"
      );

      speakResponse(
        spokenResponse
      );

    } catch (error) {
      console.error(
        "Voice command error:",
        error
      );

      setAvatarState("error");

      setStatus(
        "Something went wrong"
      );

      setResponse(
        error.message ||
          "Voice command failed."
      );
    }
  };

  // =========================================================
  // CONFIRM EMAIL SEND
  // =========================================================

  const confirmEmailSend = async () => {
  if (!pendingEmail?.confirmation_id) {
    setResponse("Confirmation ID is missing.");
    setStatus("Email sending failed");
    return;
  }

  try {
    setEmailActionLoading(true);
    setStatus("Sending email...");

    console.log(
      "Sending confirmation ID:",
      pendingEmail.confirmation_id
    );

    const res = await fetch(
      "http://127.0.0.1:8000/api/email/confirm-send",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
        },
        body: JSON.stringify({
          confirmation_id: pendingEmail.confirmation_id,
        }),
      }
    );

    const data = await res.json();

    console.log("Confirm-send response:", data);

    if (!res.ok) {
      throw new Error(
        data.detail ||
        data.message ||
        "Failed to send email."
      );
    }

    // Email was successfully sent
    setPendingEmail(null);

    setResponse(
      data.message || "Email sent successfully."
    );

    setStatus("Email sent successfully");

    speakResponse(
      data.message || "Email sent successfully."
    );

  } catch (error) {
    console.error(
      "Email confirmation error:",
      error
    );

    setResponse(
      "Email could not be sent: " +
      (error.message || "Unknown error")
    );

    setStatus("Email sending failed");

  } finally {
    setEmailActionLoading(false);
  }
};
  // =========================================================
  // CANCEL EMAIL SEND
  // =========================================================

  const cancelEmailSend = async () => {
    if (
      !pendingEmail?.confirmation_id
    ) {
      return;
    }

    try {
      setEmailActionLoading(true);

      setAvatarState("thinking");

      setStatus(
        "Cancelling email..."
      );

      const res = await fetch(
        "http://127.0.0.1:8000/api/email/cancel-send",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
            Accept:
              "application/json",
          },

          body: JSON.stringify({
            confirmation_id:
              pendingEmail.confirmation_id,
          }),
        }
      );

      const data =
        await res.json();

      if (!res.ok) {
        throw new Error(
          data.detail ||
            "Failed to cancel email"
        );
      }

      setPendingEmail(null);

      setResponse(
        data.message ||
          "Email sending cancelled."
      );

      setAvatarState("completed");

      setStatus(
        "Email cancelled"
      );

      speakResponse(
        data.message ||
          "Email sending cancelled."
      );

    } catch (error) {
      console.error(
        "Email cancellation error:",
        error
      );

      setAvatarState("error");

      setStatus(
        "Cancellation failed"
      );

      setResponse(
        error.message
      );

    } finally {
      setEmailActionLoading(
        false
      );
    }
  };

  // =========================================================
  // UI
  // =========================================================

  return (
    <div className="deskpilot">

      {/* =====================================================
          DESKPILOT 3D ROBOT
      ===================================================== */}

      <div
        className={`avatar avatar-${avatarState}`}
        onClick={() => setOpen(!open)}
        title="Open DeskPilot"
      >

        {/* Energy effects */}

        <div className="energy energy-1"></div>
        <div className="energy energy-2"></div>
        <div className="energy energy-3"></div>


        {/* Robot */}

        <div className="robot">

          {/* Antenna */}

          <div className="antenna">
            <div className="antenna-ball"></div>
          </div>


          {/* Head */}

          <div className="robot-head">

            <div className="head-shine"></div>


            {/* Left ear */}

            <div className="ear ear-left">
              <div className="ear-core"></div>
            </div>


            {/* Right ear */}

            <div className="ear ear-right">
              <div className="ear-core"></div>
            </div>


            {/* Face screen */}

            <div className="face-screen">

              <div className="eye eye-left"></div>

              <div className="eye eye-right"></div>

              <div className="robot-mouth"></div>

            </div>

          </div>


          {/* Neck */}

          <div className="neck"></div>


          {/* Body */}

          <div className="robot-body">

            <div className="body-shine"></div>

            <div className="chest-light"></div>


            {/* Arms */}

            <div className="arm arm-left"></div>

            <div className="arm arm-right"></div>

          </div>


          {/* Floating base */}

          <div className="hover-base">

            <div className="hover-light"></div>

          </div>

        </div>


        {/* Branding */}

        <div className="robot-brand">

          <span className="status-dot"></span>

          <span>DeskPilot</span>

        </div>


        {/* Status */}

        <div className="robot-status">

          {avatarState === "idle" &&
            "Ready"}

          {avatarState === "listening" &&
            "Listening"}

          {avatarState === "thinking" &&
            "Thinking"}

          {avatarState === "speaking" &&
            "Speaking"}

          {avatarState === "completed" &&
            "Completed"}

          {avatarState === "error" &&
            "Attention"}

        </div>

      </div>


      {/* =====================================================
          ASSISTANT PANEL
      ===================================================== */}

      {open && (
        <div className="assistant-panel">

          {/* Header */}

          <div className="panel-header">

            <div className="panel-title">

              <div className="panel-logo">

                <div className="panel-logo-dot"></div>

              </div>

              <div>

                <div className="panel-name">
                  DeskPilot
                </div>

                <div className="panel-subtitle">
                  AI Operating Assistant
                </div>

              </div>

            </div>


            <button
              className="close-button"
              onClick={() => setOpen(false)}
            >
              ×
            </button>

          </div>


          {/* Greeting */}

          <div className="panel-message">

            <div className="message-icon">
              DP
            </div>

            <div>

              <strong>
                Hello!
              </strong>

              <br />

              What can I do for you?

            </div>

          </div>


          {/* Status */}

          <div
            className="voice-status"
            style={{
              padding:
                "0 20px 10px",
            }}
          >
            {status}
          </div>


          {/* User transcript */}

          {transcript && (
            <div className="result-box user-result">

              <div className="result-label">
                YOU
              </div>

              <p>
                {transcript}
              </p>

            </div>
          )}


          {/* DeskPilot response */}

          {response &&
            !pendingEmail && (
              <div className="result-box">

                <div className="result-label">
                  DESKPILOT
                </div>

                <p>
                  {response}
                </p>

              </div>
            )}


          {/* =================================================
              EMAIL CONFIRMATION CARD
          ================================================= */}

          {pendingEmail && (

            <div className="email-confirmation">

              <div className="email-confirmation-header">

                <div className="email-icon">
                  ✉
                </div>

                <div>

                  <div className="email-title">
                    Confirm Email
                  </div>

                  <div className="email-subtitle">
                    Review before sending
                  </div>

                </div>

              </div>


              <div className="email-details">

                <div className="email-field">

                  <span className="email-field-label">
                    To
                  </span>

                  <span className="email-field-value">
                    {pendingEmail.recipient}
                  </span>

                </div>


                <div className="email-field">

                  <span className="email-field-label">
                    Subject
                  </span>

                  <span className="email-field-value">
                    {pendingEmail.subject}
                  </span>

                </div>


                <div className="email-body-field">

                  <span className="email-field-label">
                    Message
                  </span>

                  <div className="email-body">
                    {pendingEmail.body}
                  </div>

                </div>

              </div>


              <div className="email-warning">
                This email will not be sent until you confirm.
              </div>


              <div className="email-actions">

                <button
                  className="email-cancel-button"
                  onClick={cancelEmailSend}
                  disabled={
                    emailActionLoading
                  }
                >
                  Cancel
                </button>


                <button
                  className="email-send-button"
                  onClick={confirmEmailSend}
                  disabled={
                    emailActionLoading
                  }
                >
                  {emailActionLoading
                    ? "Processing..."
                    : "Send Email"}
                </button>

              </div>

            </div>
          )}


          {/* =================================================
              VOICE AREA
          ================================================= */}

          {!pendingEmail && (

            <div className="voice-area">

              <button
                className={`mic-button ${
                  recording
                    ? "recording"
                    : ""
                }`}
                onClick={
                  recording
                    ? stopRecording
                    : startRecording
                }
              >

                {recording
                  ? "■"
                  : "🎙"}

              </button>

              <div className="voice-status">

                {recording
                  ? "Listening..."
                  : "Click the microphone and speak"}

              </div>

            </div>

          )}

        </div>
      )}

    </div>
  );
}

export default App;