def get_client_ip(request):
    """
    Returns the real client IP address, handling proxies like Vercel or Render.
    Priority: X-Forwarded-For -> X-Real-IP -> remote_addr
    """
    if request.headers.getlist("X-Forwarded-For"):
        # X-Forwarded-For can contain a list of IPs. The first one is the client.
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
        return ip
    
    if request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    
    return request.remote_addr
