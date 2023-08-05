net.log("ESST GameGUI: loading")

package.path = package.path .. ";.\\LuaSocket\\?.lua;"
package.cpath = package.cpath .. ";.\\LuaSocket\\?.dll;"

local socket = require("socket")
local JSON = loadfile("Scripts\\JSON.lua")()
local lfs = require('lfs')
local tools = require('tools')

esst = {}

esst.json = JSON

esst.send = function(message)
    message.time = DCS.getRealTime()
    socket.try(esst.sock:sendto(esst.json:encode(message) .. '\n', '127.0.0.1', esst.port))
end

--mostly straight out of Programming in Lua
function serialize_wcycles(name, value, saved)
	local basicSerialize = function (o)
		if type(o) == "number" then
			return tostring(o)
		elseif type(o) == "boolean" then
			return tostring(o)
		elseif type(o) == "string" then
			return string.format("%q", o)
		end
	end

	local t_str = {}
	saved = saved or {}       -- initial value
	if ((type(value) == 'string') or (type(value) == 'number') or (type(value) == 'table') or (type(value) == 'boolean')) then
		table.insert(t_str, name .. " = ")
		if type(value) == "number" or type(value) == "string" or type(value) == "boolean" then
			table.insert(t_str, basicSerialize(value) ..  "\n")
		else

			if saved[value] then    -- value already saved?
				table.insert(t_str, saved[value] .. "\n")
			else
				saved[value] = name   -- save name for next time
				table.insert(t_str, "{}\n")
				for k,v in pairs(value) do      -- save its fields
					local fieldname = string.format("%s[%s]", name, basicSerialize(k))
					table.insert(t_str, serialize_wcycles(fieldname, v, saved))
				end
			end
		end
		return table.concat(t_str)
	else
		return ""
	end
end

esst.log_file = 'esst-gamegui'
esst.log_subsystem = 'esst'

esst.log_level = log.ALERT
        + log.ERROR
        + log.WARNING
        + log.INFO
        + log.DEBUG
        + log.TRACE

esst.log_output = log.FULL

log.set_output(
    esst.log_file,
    esst.log_subsystem,
    esst.log_level,
    esst.log_output
)

esst._log = function(level, message, ...)
    log.write(esst.log_subsystem, level, message, ...)
end

esst.trace =    function(message, ...) esst._log(log.TRACE,     message, ...) end
esst.debug =    function(message, ...) esst._log(log.DEBUG,     message, ...) end
esst.info =     function(message, ...) esst._log(log.INFO,      message, ...) end
esst.warning =  function(message, ...) esst._log(log.WARNING,   message, ...) end
esst.error =    function(message, ...) esst._log(log.ERROR,     message, ...) end

esst.ping_interval = 5.0
esst.ping_last_sent = 0
esst.cmd_read_interval = 1.0
esst.cmd_last_read = 0

function esst.status_update(message)
    esst.trace(message)
    esst.send({ type = 'status', message = message })
end

function esst.onMissionLoadBegin()
    esst.status_update('loading mission')
end

function esst.onMissionLoadEnd()
    esst.status_update('loaded mission')
    local now = DCS.getRealTime()
    local message = {
        type = 'mission_load',
        coalitions = DCS.getAvailableCoalitions(),
        -- slots = {
            -- 0 = DCS.getAvailableSlots(0),
            -- 1 = DCS.getAvailableSlots(1),
        -- },
        -- current_mission = DCS.getCurrentMission(),
        -- mission_options = DCS.getMissionOptions(),
    }
    --esst.send(message)
end

function esst.onSimulationStart()
    esst.status_update('starting simulation')
end

function esst.onSimulationStop()
    esst.status_update('stopping simulation')
end

function esst.onSimulationPause()
    esst.status_update('pausing simulation')
end

function esst.onSimulationResume()
    esst.status_update('resuming simulation')
end

function esst.onSimulationFrame()

    local now = DCS.getRealTime()

    if now > esst.cmd_last_read + esst.cmd_read_interval then
      esst.cmd_last_read = now
      local message = esst.cmd_sock:receive()
      if message then
          local decoded = esst.json:decode(message)
          if decoded.cmd then
              esst.info('received command: '.. decoded.cmd)
              if decoded.cmd == 'exit dcs' then
                  esst.info('closing DCS')
                  DCS.exitProcess()
              else
                  esst.error('unknown command: '.. decoded.cmd)
              end
          else
              esst.error('badly formatted command message: '.. message)
          end
      end
    end

    if now > esst.ping_last_sent + esst.ping_interval then
        esst.ping_last_sent = now
        local players = {}
        for _, player_id in ipairs(net.get_player_list()) do
            if player_id ~= 1 then
                table.insert(players, net.get_name(player_id))
            end
        end
        local message = {
            type = 'ping',
            players = players,
            model_time = DCS.getModelTime(),
            paused = DCS.getPause(),
            mission_name = DCS.getMissionName(),
            mission_filename = DCS.getMissionFilename(),
        }
        esst.send(message)
    end
end

local dediConfig = tools.safeDoFile(lfs.writedir() .. 'Config/dedicated.lua', false)
if dediConfig and dediConfig.dedicated ~= nil and dediConfig.dedicated["enabled"] == true then

    esst.debug('Creating listening socket')
    esst.sock = socket.udp()
    esst.port = {{ listener_server_port }}
    esst.sock:settimeout(0.001)

    esst.debug('Creating command socket')
    esst.cmd_sock = socket.udp()
    esst.cmd_sock:setsockname('*', {{ listener_cmd_port }})
    esst.cmd_sock:settimeout(0.001)

    esst.debug('Installing hooks')
    DCS.setUserCallbacks(esst)

    net.log("ESST GameGUI: loaded")
else
    net.log("ESST GameGUI: skipped (from configuration)")
end


