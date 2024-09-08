const API_KEY = 'your_api_key'; // Replace with actual API keys for weather and currency
    const weatherWidget = document.getElementById('weather-widget');
    const newsWidget = document.getElementById('news-widget');
    const currencyWidget = document.getElementById('currency-widget');

    // Helper function to cache data in localStorage
    const cacheData = (key, data) => {
        localStorage.setItem(key, JSON.stringify({ timestamp: Date.now(), data }));
    };

    // Helper function to retrieve cached data
    const getCachedData = (key, maxAge = 600000) => { // 10 minutes cache
        const cached = localStorage.getItem(key);
        if (!cached) return null;

        const { timestamp, data } = JSON.parse(cached);
        if (Date.now() - timestamp > maxAge) {
            localStorage.removeItem(key);
            return null;
        }
        return data;
    };

    // Fetch weather data
    const fetchWeather = async () => {
        const cachedWeather = getCachedData('weather');
        if (cachedWeather) {
            updateWeather(cachedWeather);
            return;
        }

        try {
            const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=Dhaka&appid=${API_KEY}&units=metric`);
            const data = await response.json();
            cacheData('weather', data);
            updateWeather(data);
        } catch (error) {
            showError(weatherWidget, 'Unable to fetch weather data.');
        }
    };

    const updateWeather = (data) => {
        document.getElementById('weather-temp').textContent = `${data.main.temp}°C`;
        document.getElementById('weather-desc').textContent = data.weather[0].description;
        document.querySelector('#weather-widget .loading').remove(); // Remove loading icon
    };

    // Fetch news data from Ulkaa News
    const fetchNews = async () => {
        const cachedNews = getCachedData('news');
        if (cachedNews) {
            updateNews(cachedNews);
            return;
        }

        try {
            const response = await fetch('https://news.ulkaa.com/wp-json/wp/v2/posts');
            const data = await response.json();
            cacheData('news', data);
            updateNews(data);
        } catch (error) {
            showError(newsWidget, 'Unable to fetch news.');
        }
    };

    const updateNews = (articles) => {
        const newsList = document.getElementById('news-list');
        newsList.innerHTML = articles.slice(0, 5).map(article => `
            <li class="py-2 border-b">
                <a href="${article.link}" target="_blank" class="text-blue-600">${article.title.rendered}</a>
                <p class="text-sm text-gray-500">${new Date(article.date).toLocaleTimeString()}</p>
            </li>
        `).join('');
    };

    // Fetch currency exchange data
    const fetchCurrencyRate = async () => {
        const cachedCurrency = getCachedData('currency');
        if (cachedCurrency) {
            updateCurrency(cachedCurrency);
            return;
        }

        try {
            const response = await fetch(`https://api.exchangerate-api.com/v4/latest/USD`);
            const data = await response.json();
            const rate = data.rates.BDT;
            cacheData('currency', rate);
            updateCurrency(rate);
        } catch (error) {
            showError(currencyWidget, 'Unable to fetch currency rate.');
        }
    };

    const updateCurrency = (rate) => {
        document.getElementById('currency-rate').textContent = rate.toFixed(2);
    };

    const showError = (widget, message) => {
        widget.innerHTML = `<p class="text-red-500">${message}</p>`;
    };

    document.addEventListener("DOMContentLoaded", () => {
        fetchWeather();
        fetchNews();
        fetchCurrencyRate();
    });

    // Create a calendar widget
    const calendar = document.getElementById('calendar');
    const today = new Date();
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    const renderCalendar = () => {
        const day = days[today.getDay()];
        const date = today.getDate();
        const month = months[today.getMonth()];
        const year = today.getFullYear();
        calendar.innerHTML = `
            <p class="text-2xl font-semibold">${day}</p>
            <p class="text-3xl font-bold">${date}</p>
            <p class="text-lg">${month} ${year}</p>
        `;
    };

    renderCalendar();

    // Task manager
    const tasksList = document.getElementById('tasks-list');
    tasksList.addEventListener('change', (event) => {
        if (event.target.tagName === 'INPUT') {
            const task = event.target.parentElement;
            if (event.target.checked) {
                task.style.textDecoration = 'line-through';
            } else {
                task.style.textDecoration = 'none';
            }
        }
    });

    // Background image
    const randomBackground = Math.floor(Math.random() * 6) + 1;
    document.body.style.background = `url('/img/background-${randomBackground}.jpg') no-repeat center center fixed`;
    document.body.style.backgroundSize = 'cover';


    // Update time every second
    setInterval(() => {
        const time = new Date();
        const time_el = document.getElementById('time');
        time_el.innerHTML = time.toLocaleTimeString();
    }, 1000);

    // Update weather every 10 minutes
    setInterval(fetchWeather, 600000);

    // Update news every 10 minutes
    setInterval(fetchNews, 600000);

    // Update currency rate every 10 minutes
    setInterval(fetchCurrencyRate, 600000);

    // Update calendar every day
    setInterval(() => {
        const newDate = new Date();
        if (newDate.getDate() !== today.getDate()) {
            today = newDate;
            renderCalendar();
        }
    }, 86400000);
