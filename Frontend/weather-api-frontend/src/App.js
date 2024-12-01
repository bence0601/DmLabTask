import './App.css';
import ForecastButton from './components/forecast-button';
import DailyWeatherButton from './components/daily-weather-button';
import TempBarChart from './components/bar-chart-temp';
import SearchBar from './components/city-search-bar';
import WeatherSearch from './components/city-search-bar'; 

function App() {
  return (
    <div className="App" style={{ backgroundColor: 'white', height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
      <h1></h1>
      <ForecastButton />
      <DailyWeatherButton />
      <WeatherSearch /> 
      <TempBarChart />
    </div>
  );
}

export default App;
