import httpx
import asyncio

async def send_requests():
    async with httpx.AsyncClient() as client:
        # GET request
        get_url = "http://127.0.0.1:8000"
        get_response = await client.get(get_url, params={"param1": "value1"})
        print("GET request:")
        print(f"URL: {get_url}")
        print(f"Status: {get_response.status_code}")
        print(f"Response: {get_response.text}")

        # POST request
        post_url = "http://127.0.0.1:8000/data"
        post_response = await client.post(post_url, json={"key": "value"}, headers={"Custom-Header": "value"})
        print("POST request:")
        print(f"URL: {post_url}")
        print(f"Status: {post_response.status_code}")
        print(f"Response: {post_response.text}")

        # PUT request
        put_url = "http://127.0.0.1:8000/data"
        put_response = await client.put(put_url, json={"key": "updated_value"})
        print("PUT request:")
        print(f"URL: {put_url}")
        print(f"Status: {put_response.status_code}")
        print(f"Response: {put_response.text}")

        # DELETE request
        delete_url = "http://127.0.0.1:8000/data"
        delete_response = await client.delete(delete_url, json={"key": "value"})
        print("DELETE request:")
        print(f"URL: {delete_url}")
        print(f"Status: {delete_response.status_code}")
        print(f"Response: {delete_response.text}")

        # PATCH request
        patch_url = "http://127.0.0.1:8000/data"
        patch_response = await client.patch(patch_url, json={"key": "patched_value"})
        print("PATCH request:")
        print(f"URL: {patch_url}")
        print(f"Status: {patch_response.status_code}")
        print(f"Response: {patch_response.text}")

        # HEAD request
        head_url = "http://127.0.0.1:8000"
        head_response = await client.head(head_url)
        print("HEAD request:")
        print(f"URL: {head_url}")
        print(f"Status: {head_response.status_code}")
        print(f"Headers: {head_response.headers}")

if __name__ == "__main__":
    asyncio.run(send_requests())
