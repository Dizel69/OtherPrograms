import aiohttp
import asyncio

async def send_requests():
    async with aiohttp.ClientSession() as session:
        # GET request
        get_url = "http://127.0.0.1:8000"
        async with session.get(get_url, params={"param1": "value1"}) as response:
            print("GET request:")
            print(f"URL: {get_url}")
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

        # POST request
        post_url = "http://127.0.0.1:8000/data"
        async with session.post(post_url, json={"key": "value"}, headers={"Custom-Header": "value"}) as response:
            print("POST request:")
            print(f"URL: {post_url}")
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

        # PUT request
        put_url = "http://127.0.0.1:8000/data"
        async with session.put(put_url, json={"key": "updated_value"}) as response:
            print("PUT request:")
            print(f"URL: {put_url}")
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

        # DELETE request
        delete_url = "http://127.0.0.1:8000/data"
        async with session.delete(delete_url, json={"key": "value"}) as response:
            print("DELETE request:")
            print(f"URL: {delete_url}")
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

        # PATCH request
        patch_url = "http://127.0.0.1:8000/data"
        async with session.patch(patch_url, json={"key": "patched_value"}) as response:
            print("PATCH request:")
            print(f"URL: {patch_url}")
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

        # HEAD request
        head_url = "http://127.0.0.1:8000"
        async with session.head(head_url) as response:
            print("HEAD request:")
            print(f"URL: {head_url}")
            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")

if __name__ == "__main__":
    asyncio.run(send_requests())
