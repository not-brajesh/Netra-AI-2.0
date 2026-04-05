import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [stats, setStats] = useState({
    cameras: 1,
    people: 0,
    alerts: 0,
    incidents: 0
  })

  const [alerts, setAlerts] = useState([])
  const [summary, setSummary] = useState("")
  const [page, setPage] = useState("dashboard")
  const [chat, setChat] = useState("")
  const [messages, setMessages] = useState([])



  useEffect(() => {

    fetchStats()
    fetchAlerts()
    fetchSummary()

    const interval = setInterval(() => {
      fetchStats()
      fetchAlerts()
      fetchSummary()
    }, 3000)

    return () => clearInterval(interval)

  }, [])



  const fetchStats = async () => {

    try {

      const res = await axios.get("http://localhost:8000/status")

      setStats({
        cameras: 1,
        people: res.data.people || 0,
        alerts: res.data.alerts || 0,
        incidents: res.data.incidents || 0
      })

    } catch (e) { }

  }



  const fetchAlerts = async () => {

    try {

      const res = await axios.get("http://localhost:8000/alerts")

      setAlerts(res.data || [])

    } catch (e) { }

  }



  const fetchSummary = async () => {

    try {

      const res = await axios.get("http://localhost:8000/summary")

      setSummary(res.data.summary)

    } catch (e) { }

  }



  const sendChat = async () => {

    if (!chat) return

    const user = { type: "user", text: chat }
    setMessages(prev => [...prev, user])

    const res = await axios.post("http://localhost:8000/chat", {
      query: chat
    })

    const bot = { type: "bot", text: res.data.answer }

    setMessages(prev => [...prev, user, bot])

    setChat("")

  }



  return (

    <div className="app">


      {/* Sidebar */}

      <div className="sidebar">

        <h2>NETRA-AI</h2>

        <ul>

          <li onClick={() => setPage("dashboard")}>🏠 Dashboard</li>
          <li onClick={() => setPage("camera")}>📹 Live Camera</li>
          <li onClick={() => setPage("alerts")}>🚨 Alerts</li>
          <li onClick={() => setPage("analytics")}>📊 Analytics</li>
          <li onClick={() => setPage("reports")}>📁 Reports</li>
          <li onClick={() => setPage("chat")}>🤖 AI Chat</li>

        </ul>

      </div>



      <div className="main">

        <div className="topbar">
          NETRA-AI Smart Surveillance System
        </div>



        {/* DASHBOARD */}

        {page === "dashboard" && (

          <div className="dashboard">


            <div className="cards">

              <Card title="Live Cameras" value={stats.cameras} />
              <Card title="People Detected" value={stats.people} />
              <Card title="Alerts" value={stats.alerts} />
              <Card title="Incidents" value={stats.incidents} />

            </div>



            <div className="camera">

              <h3>Live Camera Feed</h3>

              <img
                src="http://localhost:8000/video"
                className="camera-feed"
              />

            </div>



            <div className="alerts">

              <h3>Live Alerts</h3>

              {alerts.map((a, i) => (
                <div key={i} className="alert flash">
                  🚨 {a}
                </div>
              ))}

            </div>



            <div className="summary">

              <h3>AI Summary</h3>

              <div className="summary-box">

                <ul>

                  {summary.split("\n").map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}

                </ul>

              </div>

            </div>


          </div>

        )}



        {/* CHAT */}

        {page === "chat" && (

          <div className="chat">

            <h3>AI Surveillance Chat</h3>

            <div className="chat-box">

              {messages.map((m, i) => (
                <div key={i} className={m.type}>
                  {m.text}
                </div>
              ))}

            </div>

            <input
              value={chat}
              onChange={(e) => setChat(e.target.value)}
              placeholder="Ask like: 5 PM kon aaya tha"
            />

            <button onClick={sendChat}>
              Send
            </button>

          </div>

        )}



      </div>

    </div>

  )

}



const Card = ({ title, value }) => (

  <div className="card">
    <h4>{title}</h4>
    <h2>{value}</h2>
  </div>

)

export default App