import uvicorn
from pcap_network.NetFrenzy import pipeline
from fastapi import FastAPI, Request

app = FastAPI(description="Password Finder API")

"""
Routes
"""

FILE = "pcap_files/network.pcap"


# API endpoint
@app.post("/pcap")
async def pcap(request:Request):
    data = await request.body()
    with open("pcap_files/network.pcap", "wb") as binary_file:
        # Write bytes to file
        binary_file.write(data)
    pipeline(FILE)
    return {"status":"Complete"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
