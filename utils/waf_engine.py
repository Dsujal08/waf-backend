import re
from models.rule import list_rules
from models.log import log_request
from models.alert import create_alert
from sockets.socketio_app import broadcast_alert
from utils.rate_limiter import hit as rate_hit

COMMON = {
    "sqli": re.compile(r"('(\s|;|--)|(\bUNION\b)|(\bSELECT\b.*\bFROM\b)|(\bOR\b\s+\d+=\d+))", re.IGNORECASE),
    "xss": re.compile(r"(<script\b[^>]*>.*?</script>)|(<.*on\w+=)", re.IGNORECASE),
    "path_traversal": re.compile(r"(\.\./|\.\.\\)")
}

def inspect_request(req):
    ip = req.headers.get("X-Forwarded-For", req.remote_addr)
    endpoint = req.path
    method = req.method
    try:
        payload_str = str(req.get_json(silent=True)) if req.is_json else (req.get_data(as_text=True) or str(req.args.to_dict()))
    except Exception:
        payload_str = req.get_data(as_text=True) or str(req.args.to_dict())

    # rate limit check
    if rate_hit(ip):
        reason = {"type":"rate-limit","action":"block","description":"Rate limit exceeded"}
        log_request({"method":method,"ip":ip,"endpoint":endpoint,"payload":payload_str,"isBlocked":True,"ruleTriggered":reason,"severity":"high"})
        create_alert({"message": reason["description"], "ip": ip, "endpoint": endpoint, "rule": reason, "severity": "high"})
        broadcast_alert({"message": reason["description"], "ip": ip, "endpoint": endpoint, "rule": reason, "severity": "high"})
        return True, reason

    # DB rules
    for r in list_rules():
        if not r.get("isActive", True): continue
        rtype = r.get("type","regex")
        action = r.get("action","block")
        pattern = r.get("pattern","")
        if rtype == "ip-block" and ip == pattern:
            log_request({"method":method,"ip":ip,"endpoint":endpoint,"payload":payload_str,"isBlocked": action=="block","ruleTriggered":r,"severity":"high"})
            if action=="block":
                create_alert({"message":"IP blocked by rule","ip":ip,"rule":r,"severity":"high"})
                broadcast_alert({"message":"IP blocked by rule","ip":ip,"rule":r,"severity":"high"})
            return action=="block", r
        else:
            try:
                pat = re.compile(pattern, re.IGNORECASE) if pattern else None
                if pat and pat.search(payload_str + " " + endpoint):
                    log_request({"method":method,"ip":ip,"endpoint":endpoint,"payload":payload_str,"isBlocked": action=="block","ruleTriggered":r,"severity":"medium"})
                    if action=="block":
                        create_alert({"message":"Rule triggered: "+r.get("name","rule"),"ip":ip,"rule":r,"severity":"medium"})
                        broadcast_alert({"message":"Rule triggered: "+r.get("name","rule"),"ip":ip,"rule":r,"severity":"medium"})
                    return action=="block", r
            except re.error:
                continue

    # heuristics
    for name, pat in COMMON.items():
        if pat.search(payload_str + " " + endpoint):
            reason = {"type":name,"action":"block","description":f"{name} matched"}
            log_request({"method":method,"ip":ip,"endpoint":endpoint,"payload":payload_str,"isBlocked":True,"ruleTriggered":reason,"severity":"high"})
            create_alert({"message":reason["description"],"ip":ip,"endpoint":endpoint,"rule":reason,"severity":"high"})
            broadcast_alert({"message":reason["description"],"ip":ip,"endpoint":endpoint,"rule":reason,"severity":"high"})
            return True, reason

    # allowed
    log_request({"method":method,"ip":ip,"endpoint":endpoint,"payload":payload_str,"isBlocked":False,"ruleTriggered":None,"severity":"info"})
    return False, None
