import './App.css'
import ChatApp from './components/ChatApp'

const App = () => {
  const styles = {
    backgroundColor: '#f8fafc',
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
  }

  return (
    <div style={styles}>
      <div className='flex justify-center pt-10'>
      <h1 style={{
          fontFamily: 'monospace',
          textAlign: 'center',
          fontSize: '2rem',
          fontWeight: 'bold',
          color: '#2d3748',
          textShadow: '2px 2px #cbd5e0'
          }}>
          chatboy
        </h1>
      </div>
      <ChatApp />
    </div>
  )
}

export default App