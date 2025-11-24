const API_KEY = 'your_api_key';
const weatherWidget = document.getElementById('weather-widget');
const newsWidget = document.getElementById('news-widget');
const currencyWidget = document.getElementById('currency-widget');

// Search widget
const searchInput = document.getElementById('search-widget');
if (searchInput) {
	searchInput.addEventListener('keypress', (event) => {
		if (event.key === 'Enter') {
			search(searchInput.value);
		}
	});
}

const search = async (query) => {
	try {
		const isURL = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i.test(query);
		if (isURL) {
			window.location.href = query;
			return;
		} else {
			window.location.href = 'https://www.google.com/search?q=' + query;
		}
	} catch (error) {
		console.error(error);
	}
};

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
		// Fail silently or show minimal error to keep UI clean
		console.error('Unable to fetch weather data.');
	}
};

const updateWeather = (data) => {
	const tempEl = document.getElementById('weather-temp');
	const descEl = document.getElementById('weather-desc');
	const loader = document.querySelector('#weather-widget .loading');

	if (tempEl) tempEl.textContent = `${Math.round(data.main.temp)}°C`;
	if (descEl) descEl.textContent = data.weather[0].description;
	if (loader) loader.remove();
};

// Fetch news data from Ulkaa News
const fetchNews = async () => {
	const cachedNews = getCachedData('news');
	if (cachedNews) {
		updateNews(cachedNews);
		return;
	}

	try {
		const response = await fetch('https://news.ulkaa.com/wp-json/wp/v2/posts?_fields=title,link,date&per_page=6');
		const data = await response.json();
		cacheData('news', data);
		updateNews(data);
	} catch (error) {
		console.error('Unable to fetch news.');
	}
};

const updateNews = (articles) => {
	const newsList = document.getElementById('news-list');
	if (!newsList) return;

	newsList.innerHTML = articles.map(article => `
        <li class="group">
            <a href="${article.link}" target="_blank" class="block p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-all border border-white/5 hover:border-white/20">
                <h3 class="text-gray-200 group-hover:text-green-400 font-medium transition-colors line-clamp-2 mb-2">${article.title.rendered}</h3>
                <p class="text-xs text-gray-500">
                    ${new Date(article.date).toLocaleString('en-US', { dateStyle: 'medium' })}
                </p>
            </a>
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
		console.error('Unable to fetch currency rate.');
	}
};

const updateCurrency = (rate) => {
	const rateEl = document.getElementById('currency-rate');
	if (rateEl) rateEl.textContent = `৳ ${rate.toFixed(2)}`;
};

// Neuron Animation (Canvas)
const initNeuronAnimation = () => {
	const canvas = document.getElementById('neuron-canvas');
	if (!canvas) return;

	const ctx = canvas.getContext('2d');
	let w, h;
	const mouse = { x: 0, y: 0 };

	const resize = () => {
		w = canvas.width = window.innerWidth;
		h = canvas.height = window.innerHeight;
	};

	window.addEventListener('resize', resize);
	resize();

	window.addEventListener('mousemove', (e) => {
		mouse.x = e.clientX;
		mouse.y = e.clientY;
	});

	const nodes = Array.from({ length: 100 }, () => ({
		x: Math.random() * w,
		y: Math.random() * h,
		vx: Math.random() * 1.5 - 0.75,
		vy: Math.random() * 1.5 - 0.75,
		r: 1.5 + Math.random() * 2,
		pulse: Math.random() * Math.PI * 2
	}));

	const animate = () => {
		ctx.clearRect(0, 0, w, h);

		nodes.forEach((p, i) => {
			// Mouse attraction
			const dx = mouse.x - p.x;
			const dy = mouse.y - p.y;
			const dist = Math.sqrt(dx * dx + dy * dy);

			if (dist < 200) {
				p.vx += dx * 0.0002;
				p.vy += dy * 0.0002;
			}

			p.x += p.vx;
			p.y += p.vy;

			// Bounce off walls
			if (p.x < 0 || p.x > w) p.vx *= -1;
			if (p.y < 0 || p.y > h) p.vy *= -1;

			// Pulsing effect
			p.pulse += 0.05;
			const pulseSize = p.r + Math.sin(p.pulse) * 0.5;

			// Draw node
			ctx.beginPath();
			ctx.arc(p.x, p.y, pulseSize, 0, Math.PI * 2);
			const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, pulseSize * 2);
			gradient.addColorStop(0, '#39FF14');
			gradient.addColorStop(0.5, 'rgba(57, 255, 20, 0.4)');
			gradient.addColorStop(1, 'rgba(57, 255, 20, 0)');
			ctx.fillStyle = gradient;
			ctx.fill();

			// Draw connections
			for (let j = i + 1; j < nodes.length; j++) {
				const q = nodes[j];
				const dx = p.x - q.x;
				const dy = p.y - q.y;
				const dist = Math.sqrt(dx * dx + dy * dy);
				if (dist < 150) {
					const opacity = 1 - dist / 150;
					ctx.beginPath();
					ctx.moveTo(p.x, p.y);
					ctx.lineTo(q.x, q.y);
					const lineGradient = ctx.createLinearGradient(p.x, p.y, q.x, q.y);
					lineGradient.addColorStop(0, `rgba(57, 255, 20, ${opacity * 0.2})`);
					lineGradient.addColorStop(0.5, `rgba(168, 85, 247, ${opacity * 0.15})`);
					lineGradient.addColorStop(1, `rgba(6, 182, 212, ${opacity * 0.2})`);
					ctx.strokeStyle = lineGradient;
					ctx.lineWidth = 1;
					ctx.stroke();
				}
			}
		});

		requestAnimationFrame(animate);
	};

	animate();
};

// Analog Clock
const initClock = () => {
	const clock = document.getElementById('clock-widget');
	if (!clock) return;

	const ctx = clock.getContext('2d');
	let radius = clock.height / 2;
	ctx.translate(radius, radius);
	radius = radius * 0.90;

	const drawClock = () => {
		drawFace(ctx, radius);
		drawNumbers(ctx, radius);
		drawTime(ctx, radius);
	};

	const drawFace = (ctx, radius) => {
		ctx.beginPath();
		ctx.arc(0, 0, radius, 0, 2 * Math.PI);
		ctx.fillStyle = 'rgba(0, 0, 0, 0.3)'; // Dark semi-transparent face
		ctx.fill();

		ctx.strokeStyle = '#A855F7'; // Purple border
		ctx.lineWidth = radius * 0.05;
		ctx.stroke();

		ctx.beginPath();
		ctx.arc(0, 0, radius * 0.05, 0, 2 * Math.PI);
		ctx.fillStyle = '#39FF14'; // Green center dot
		ctx.fill();
	};

	const drawNumbers = (ctx, radius) => {
		let ang;
		let num;
		ctx.font = 'bold ' + radius * 0.15 + 'px Inter';
		ctx.textBaseline = 'middle';
		ctx.textAlign = 'center';
		ctx.fillStyle = '#FFFFFF'; // White numbers

		for (num = 1; num < 13; num++) {
			ang = num * Math.PI / 6;
			ctx.rotate(ang);
			ctx.translate(0, -radius * 0.85);
			ctx.rotate(-ang);
			ctx.fillText(num.toString(), 0, 0);
			ctx.rotate(ang);
			ctx.translate(0, radius * 0.85);
			ctx.rotate(-ang);
		}
	};

	const drawTime = (ctx, radius) => {
		const now = new Date();
		let hour = now.getHours();
		let minute = now.getMinutes();
		let second = now.getSeconds();

		hour = hour % 12;
		hour = (hour * Math.PI / 6) + (minute * Math.PI / (6 * 60)) + (second * Math.PI / (360 * 60));
		drawHand(ctx, hour, radius * 0.5, radius * 0.07, '#FFFFFF'); // Hour hand

		minute = (minute * Math.PI / 30) + (second * Math.PI / (30 * 60));
		drawHand(ctx, minute, radius * 0.8, radius * 0.05, '#06B6D4'); // Minute hand (Cyan)

		second = (second * Math.PI / 30);
		drawHand(ctx, second, radius * 0.9, radius * 0.02, '#39FF14'); // Second hand (Green)
	};

	const drawHand = (ctx, pos, length, width, color) => {
		ctx.beginPath();
		ctx.lineWidth = width;
		ctx.lineCap = 'round';
		ctx.strokeStyle = color;
		ctx.moveTo(0, 0);
		ctx.rotate(pos);
		ctx.lineTo(0, -length);
		ctx.stroke();
		ctx.rotate(-pos);
	};

	setInterval(drawClock, 1000);
	drawClock();
};

// Calendar Widget
const initCalendar = () => {
	const calendar = document.getElementById('calendar');
	if (!calendar) return;

	const today = new Date();
	const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
	const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

	const renderCalendar = () => {
		const day = days[today.getDay()];
		const date = today.getDate();
		const month = months[today.getMonth()];
		const year = today.getFullYear();

		calendar.innerHTML = `
            <div class="flex flex-col items-center">
                <p class="text-lg font-medium text-blue-300 uppercase tracking-wider mb-1">${day}</p>
                <p class="text-6xl font-black text-white mb-2 drop-shadow-lg">${date}</p>
                <p class="text-sm text-gray-400">${month} ${year}</p>
            </div>
        `;
	};

	renderCalendar();
};

// Initialization
document.addEventListener("DOMContentLoaded", () => {
	fetchWeather();
	fetchNews();
	fetchCurrencyRate();
	initNeuronAnimation();
	initClock();
	initCalendar();

	// Update time every second
	setInterval(() => {
		const time = new Date();
		const time_el = document.getElementById('time');
		if (time_el) time_el.innerHTML = time.toLocaleTimeString();
	}, 1000);

	// Refresh data periodically
	setInterval(fetchWeather, 600000);
	setInterval(fetchNews, 600000);
	setInterval(fetchCurrencyRate, 600000);
});
