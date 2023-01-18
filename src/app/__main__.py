import uvicorn

if __name__ == '__main__':
    uvicorn.run('app.backend:app', host='0.0.0.0', port=30002, reload=True)