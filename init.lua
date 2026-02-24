local drawing = require("hs.drawing")
local geometry = require("hs.geometry")
local window = require("hs.window")
local fnutils = require("hs.fnutils")

local BUTTON_SIZE = 22
local TITLEBAR_HEIGHT = 28 -- approximate
local windowButtons = {}

local function createXPButton(win, imgPath, callback, offset)
    local f = win:frame()
    local btn = drawing.image(
        geometry.rect(
            f.x + 10 + offset, -- LEFT side
            f.y + (TITLEBAR_HEIGHT - BUTTON_SIZE)/2,
            BUTTON_SIZE,
            BUTTON_SIZE
        ),
        hs.image.imageFromPath(imgPath)
    )
    btn:setLevel(drawing.windowLevels.overlay)
    btn:show()
    btn:setClickCallback(callback)
    return btn
end

local function removeButtons(win)
    local id = win:id()
    if windowButtons[id] then
        for _, b in ipairs(windowButtons[id]) do b:delete() end
        windowButtons[id] = nil
    end
end

local function addXPButtons(win)
    if not win:isStandard() then return end
    removeButtons(win)
    local buttons = {}
    table.insert(buttons, createXPButton(win, "/Users/ayoub/themes/close.png", function() win:close() end, 0))
    table.insert(buttons, createXPButton(win, "/Users/ayoub/themes/minimize.png", function() win:minimize() end, 30))
    table.insert(buttons, createXPButton(win, "/Users/ayoub/themes/maximize.png", function()
        if win:isFullScreen() then win:unmaximize() else win:maximize() end
    end, 60))
    windowButtons[win:id()] = buttons
end

local function updatePositions(win)
    local buttons = windowButtons[win:id()]
    if not buttons then return end
    local f = win:frame()
    for i, b in ipairs(buttons) do
        local offset = (i-1) * 30
        b:setFrame(geometry.rect(
            f.x + 10 + offset, -- LEFT side
            f.y + (TITLEBAR_HEIGHT - BUTTON_SIZE)/2,
            BUTTON_SIZE,
            BUTTON_SIZE
        ))
    end
end

local wf = hs.window.filter.default
wf:subscribe({"windowFocused", "windowMoved"}, function(win)
    if win:isStandard() then addXPButtons(win) end
    updatePositions(win)
end)
wf:subscribe("windowDestroyed", removeButtons)

hs.hotkey.bind({"cmd","alt","ctrl"}, "R", function() hs.reload() end)
hs.alert.show("XP Buttons Overlay Loaded on LEFT SIDE!")