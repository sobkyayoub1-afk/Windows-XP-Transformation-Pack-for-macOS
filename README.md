Bring back the nostalgia of Windows XP on your Mac with classic XP-style window buttons, plus a fun retro taskbar! This project uses Hammerspoon to overlay XP-style Close, Minimize, and Maximize buttons on macOS windows, and a text-based taskbar for the full retro feel.

⚡ Features

XP-style Close, Minimize, and Maximize buttons on all standard macOS windows.

Buttons follow the window when moved or resized.

Buttons disappear when the window is closed.

Fully customizable: use your own XP-style button image pack.

Classic taskbar coded in collaboration with ChatGPT — brings that retro text-based XP look to your desktop.

🛠 Installation

Install Hammerspoon
.

Place your XP-style button images somewhere on your system (e.g., ~/xp-buttons/close.png).

Update the Lua script paths in init.lua:

-- Example paths in your script:
createXPButton(win, "/path/to/your/close.png", function() win:close() end, 0)
createXPButton(win, "/path/to/your/minimize.png", function() win:minimize() end, 30)
createXPButton(win, "/path/to/your/maximize.png", function()
    if win:isFullScreen() then win:unmaximize() else win:maximize() end
end, 60)

⚠ Make sure to replace /path/to/your/ with the folder containing your button image pack. This is required for the XP buttons to appear correctly.

Reload Hammerspoon (Cmd+Alt+Ctrl+R) or restart the app.

Focus a window to see the XP buttons appear on the right side of the window.

Enjoy the classic taskbar at the bottom of your screen — fully customizable via the Lua script.

🎨 Customization

Change button positions by editing the updatePositions function in the Lua script.

Replace the button images with your own XP-style icons.

Adjust BUTTON_SIZE and TITLEBAR_HEIGHT if needed for different screen resolutions.

Modify the  taskbar text or styling directly in the Lua script to suit your retro aesthetic.

📌 Assets & Credits

XP-style buttons: Inspired by the Reborn XP Windows XP simulator → https://xp.quenq.com/

Classic taskbar: Coded by Ayoub in collaboration with ChatGPT.

These assets are not included in this repository. You need to provide your own button image pack. This project is not affiliated with Microsoft.

📜 License

The Lua script in this repository is licensed under the MIT License.

The XP-style assets are not included and remain the property of their original sources (Reborn XP / Quenq). Use your own images to comply with copyright rules.








⚠ Deprecated: window.py

The window.py script is a legacy Python file from older versions of this project and is no longer functional.

Important:

Using it may break XP button overlays, duplicate buttons, or conflict with the ASCII taskbar.

It is retained only for historical reference and should not be executed under any circumstances.

Use the current Lua script instead:

Handles XP-style Close, Minimize, and Maximize buttons

Fully compatible with the  taskbar

Updates dynamically when windows move, resize, or close

⚡ Tip: Always reference your XP button images in the current Lua script; do not attempt to revive window.py.


⚠ Known Bug – Random XP Buttons

Some users may occasionally see random XP-style “X” buttons appear on the screen where no window exists. This is due to a Hammerspoon-related quirk with the current button overlay system.

What to do if this happens:

Simply click the random X button to close it.

Once all the stray buttons are closed, they will not appear again until the script is reloaded.

We are aware of this issue and plan to address it in a future update. In the meantime, closing the zombie buttons manually is the safe workaround.





🖱 Optional Mousecape Cursor Pack

If you want a complete Windows XP experience, you can also use the optional Mousecape cursor pack.

Important notes:

The cursor pack does not come bundled with the main release you download from the Releases tab.

To use it, you need Mousecape (if you are having issues with Macos 26 use this version https://github.com/AdamWawrzynkowskiGF/Mousecape-TahoeSupport/releases/tag/PreRelease-v01)
The optional .mousecape file is included in the source code. You can find it in the repository and install it manually.

Once installed, your cursors will match the Windows XP theme along with the XP-style buttons.
