const puppeteer = require('puppeteer')


const MEMORY_SETTINGS = ['--unlimited-storage', '--full-memory-crash-report', '--disable-dev-shm-usage']
const SANDBOX = ['--no-sandbox', '--disable-setuid-sandbox', '--disable-features=VizDisplayCompositor']
const UBUNTU = ['--disable-gpu', '--disable-software-rasterizer']

const urls = [
    'https://example.com',
    'https://reddit.com',
    'https://google.com',
    'https://facebook.com',

]

const mapSeries = async (iterable, action) => {
    for (const x of iterable) {
        await action(x)
    }
}



const main = async () => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: '/usr/bin/chromium-browser',
        dumpio: true,
        args: [...MEMORY_SETTINGS, ...SANDBOX, ...UBUNTU]
    })

    const page = await browser.newPage()

    mapSeries(urls, async (url) => {
        console.log(`Going to ${url}`)

        await page.goto(url)

        console.log('Taking picture!')
        await page.screenshot({
            path: `screenshots/${url.split('//')[1]}.png`
        })

        console.log(`Done with ${url}`)
    })
}

main() 