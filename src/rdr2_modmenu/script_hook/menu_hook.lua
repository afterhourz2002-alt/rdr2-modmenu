-- rdr2-modmenu script hook — runs inside RDR2 via ScriptHookRDR2
-- queues feature toggles into a named pipe read by memory_bridge.rdr2_bridge

local pipe = "\\\\.\\pipe\\rdr2_modmenu_cmd"

local function push(feature, args)
    local f = io.open(pipe, "w")
    if not f then return end
    f:write(string.format('{"feature":"%s","args":%s,"ts":%.3f}\n',
        feature, args or "{}", os.clock()))
    f:close()
end

RegisterKeyMapping("+rdr2modmenu_toggle", "Toggle ModMenu", "keyboard", "F5")
RegisterKeyMapping("+rdr2modmenu_god", "Godmode", "keyboard", "F1")
RegisterKeyMapping("+rdr2modmenu_noclip", "Noclip", "keyboard", "F2")

Citizen.CreateThread(function()
    while true do
        Citizen.Wait(0)
        if IsControlJustPressed(0, 0x8CC9CD42) then push("godmode", '{"enabled":true}') end
        if IsControlJustPressed(0, 0x8CC9CD42) then push("noclip",  '{"enabled":true}') end
    end
end)