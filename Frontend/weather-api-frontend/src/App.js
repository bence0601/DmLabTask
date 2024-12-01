import './App.css';
import ForecastButton from './components/forecast-button';
import DailyWeatherButton from './components/daily-weather-button';
import TempBarChart from './components/bar-chart-temp';
import SearchBar from './components/city-searc-bar';

function App() {
  return (
    <div className="App" style={{ backgroundColor: 'white', height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
      <h1>Hello, this is my React project</h1>
      <ForecastButton />
      <DailyWeatherButton/>
      <TempBarChart/>
      <SearchBar/>
    </div>
  );
}
  
export default App;
