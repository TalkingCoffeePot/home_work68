

async function makeRequest(url, method = 'POST') {
    let response = await fetch(url, {method})

    if (response.ok) {
        return await response.json()
    } else {
        console.log('error')
    }
}


