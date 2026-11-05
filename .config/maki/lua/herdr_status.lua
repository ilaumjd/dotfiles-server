-- Herdr OSC 7501 reporting for Maki on Linux.
-- Child jobs have piped output and a new session; write through Maki's stdout.
local last = nil
local function report(state)
  if state == last then return end
  local job, err = maki.fn.jobstart({"/bin/sh", "-c",
    'printf "\\033]7501;state=%s:app=maki\\033\\\\" "$1" > "/proc/$PPID/fd/1"',
    "herdr-status", state})
  if not job then maki.log.warn("Herdr status: " .. tostring(err)); return end
  local result, wait_err = maki.fn.jobwait(job, 2000)
  if result and result.exit_code == 0 then last = state
  else maki.log.warn("Herdr status failed: " .. tostring(wait_err or (result and result.stderr))) end
end
local function sync()
  local session = maki.session.read()
  if not session then return end
  local states = {working = "working", needs_input = "blocked", idle = "idle"}
  report(states[session.status] or "idle")
end
maki.api.create_autocmd({"SessionStatusChanged", "SessionFocusChanged"}, {callback = sync})
maki.api.create_autocmd("TurnError", {callback = function() report("error") end})
return {}
