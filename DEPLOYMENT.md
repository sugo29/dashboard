# Deployment Guide for Dashboard Navigation

This guide explains how to configure navigation between dashboards when deployed to different platforms.

## 🚀 Deployment Options

### 1. **Streamlit Cloud** (Recommended)

**Steps:**
1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy both dashboards as separate apps:
   - `kitchen_dashboard.py` → `https://your-kitchen-dashboard.streamlit.app`
   - `vardashboard.py` → `https://your-variance-dashboard.streamlit.app`

**Configuration:**
In Streamlit Cloud settings, add these secrets:
```toml
KITCHEN_DASHBOARD_URL = "https://your-kitchen-dashboard.streamlit.app"
VARIANCE_DASHBOARD_URL = "https://your-variance-dashboard.streamlit.app"
```

### 2. **Heroku**

**Steps:**
1. Create two Heroku apps
2. Deploy each dashboard separately
3. Set environment variables:

```bash
# For Kitchen Dashboard App
heroku config:set KITCHEN_DASHBOARD_URL=https://your-kitchen-dashboard.herokuapp.com
heroku config:set VARIANCE_DASHBOARD_URL=https://your-variance-dashboard.herokuapp.com

# For Variance Dashboard App  
heroku config:set KITCHEN_DASHBOARD_URL=https://your-kitchen-dashboard.herokuapp.com
heroku config:set VARIANCE_DASHBOARD_URL=https://your-variance-dashboard.herokuapp.com
```

### 3. **Docker + Cloud Provider**

**Docker Setup:**
```dockerfile
# Dockerfile for Kitchen Dashboard
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "kitchen_dashboard.py", "--server.port=8501"]

# Dockerfile for Variance Dashboard  
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8502
CMD ["streamlit", "run", "vardashboard.py", "--server.port=8502"]
```

**Environment Variables:**
```bash
KITCHEN_DASHBOARD_URL=https://kitchen.yourdomain.com
VARIANCE_DASHBOARD_URL=https://variance.yourdomain.com
```

### 4. **Single Server Deployment**

If deploying both dashboards on the same server:

```bash
# Start Kitchen Dashboard
streamlit run kitchen_dashboard.py --server.port 8501 &

# Start Variance Dashboard  
streamlit run vardashboard.py --server.port 8502 &
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location /kitchen {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
    }
    
    location /variance {
        proxy_pass http://localhost:8502;
        proxy_set_header Host $host;
    }
}
```

## 🔧 Configuration Guide

### Local Development
No changes needed - uses default localhost URLs.

### Production Deployment
Update the `.streamlit/secrets.toml` file with your deployed URLs:

```toml
KITCHEN_DASHBOARD_URL = "https://your-actual-kitchen-url.com"
VARIANCE_DASHBOARD_URL = "https://your-actual-variance-url.com"
```

### Environment Variables (Alternative)
Instead of secrets.toml, you can set environment variables:

```bash
export KITCHEN_DASHBOARD_URL="https://your-kitchen-url.com"
export VARIANCE_DASHBOARD_URL="https://your-variance-url.com"
```

## 🌐 Navigation Features

### ✅ What Works in Deployment:
- **Direct URL Links**: Clickable buttons that open new tabs
- **Cross-Domain Navigation**: Works between different subdomains/domains
- **Environment Detection**: Automatically detects local vs production
- **Configurable URLs**: Easy to update URLs for different environments

### 🔄 Navigation Flow:
1. User clicks navigation button
2. New tab opens with target dashboard
3. Target dashboard loads with proper navigation
4. Users can switch back and forth seamlessly

## 📋 Deployment Checklist

- [ ] Update `secrets.toml` with production URLs
- [ ] Test navigation locally
- [ ] Deploy both dashboards
- [ ] Verify cross-navigation works
- [ ] Update URLs in secrets/environment variables
- [ ] Test final deployment

## 🎯 Best Practices

1. **Use HTTPS**: Ensure all URLs use HTTPS in production
2. **Consistent Naming**: Use clear, consistent naming for dashboard URLs
3. **Environment Variables**: Keep URLs configurable for different environments
4. **Testing**: Always test navigation after deployment
5. **Monitoring**: Monitor both dashboards for availability

## 🔍 Troubleshooting

**Navigation not working?**
- Check if URLs in secrets.toml are correct
- Verify both dashboards are accessible
- Check browser console for errors
- Ensure HTTPS/HTTP consistency

**Button not clickable?**
- Check HTML rendering in browser
- Verify CSS styles are applied
- Test in different browsers

**Wrong environment detected?**
- Check secrets.toml configuration
- Verify environment variables are set
- Restart the application after changes
