const {
    app,
    BrowserWindow,
    screen
} = require("electron");

const path = require("path");

let mainWindow;


function createWindow() {

    const display = screen.getPrimaryDisplay();

    const { width, height } = display.workAreaSize;

    mainWindow = new BrowserWindow({
        width: 400,
        height: 500,

        x: width - 420,
        y: height - 520,

        frame: false,

        transparent: true,

        backgroundColor: "#00000000",

        resizable: false,

        movable: false,

        alwaysOnTop: true,

        skipTaskbar: true,

        hasShadow: false,

        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        }
    });

    // Development mode
    mainWindow.loadURL("http://localhost:5173");

    // Keep DeskPilot above other windows
    mainWindow.setAlwaysOnTop(true, "floating");

    mainWindow.on("closed", () => {
        mainWindow = null;
    });
}


app.whenReady().then(() => {

    createWindow();

    app.on("activate", () => {

        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }

    });

});


app.on("window-all-closed", () => {

    if (process.platform !== "darwin") {
        app.quit();
    }

});