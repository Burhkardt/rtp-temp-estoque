import { useState, useRef } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [activeTab, setActiveTab] = useState<'auth' | 'qrcode' | 'barcode' | 'whatsapp'>('auth')
  const [user, setUser] = useState<{username: string} | null>(null)
  
  // Auth State
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  
  // QR State
  const [recordId, setRecordId] = useState('')
  const [qrCode, setQrCode] = useState('')
  const [decodedData, setDecodedData] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Barcode State
  const [barcodeData, setBarcodeData] = useState('')
  const [barcodeImg, setBarcodeImg] = useState('')
  const [decodedBarcode, setDecodedBarcode] = useState('')
  const barcodeFileInputRef = useRef<HTMLInputElement>(null)
  
  // WhatsApp State
  const [phone, setPhone] = useState('')
  const [message, setMessage] = useState('')
  const [sendResult, setSendResult] = useState<any>(null)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      const data = await res.json()
      if (data.token) {
        setUser({ username })
        setActiveTab('qrcode')
      }
    } catch (err) {
      alert('Erro ao conectar com backend')
    }
  }

  const handleGenerateQR = async () => {
    if (!recordId) return
    try {
      const res = await fetch(`${API_URL}/qrcode/generate/${recordId}`)
      const data = await res.json()
      setQrCode(data.qr_code_base64)
    } catch (err) {
      alert('Erro ao gerar QR Code')
    }
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_URL}/qrcode/read`, {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      if (data.decoded_data) {
        setDecodedData(data.decoded_data)
      } else {
        alert(data.detail || 'Não foi possível ler o QR Code')
      }
    } catch (err) {
      alert('Erro ao ler QR Code')
    }
  }

  const handleGenerateBarcode = async () => {
    if (!barcodeData) return
    try {
      const res = await fetch(`${API_URL}/barcode/generate/${barcodeData}`)
      const data = await res.json()
      setBarcodeImg(data.barcode_base64)
    } catch (err) {
      alert('Erro ao gerar Código de Barras')
    }
  }

  const handleBarcodeFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch(`${API_URL}/barcode/read`, {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      if (data.decoded_data) {
        setDecodedBarcode(data.decoded_data)
      } else {
        alert(data.detail || 'Não foi possível ler o código de barras')
      }
    } catch (err) {
      alert('Erro ao ler código de barras')
    }
  }

  const handleSendMessage = async () => {
    try {
      const res = await fetch(`${API_URL}/messaging/whatsapp/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ to_number: phone, message })
      })
      const data = await res.json()
      setSendResult(data)
    } catch (err) {
      alert('Erro ao enviar mensagem')
    }
  }

  return (
    <div className="app-container">
      <div className="sidebar">
        <h1>Softex Pro</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
          Sistema Integrado de Leitura e Envio WhatsApp
        </p>
        
        {user ? (
          <div className="card" style={{ padding: '1rem', marginBottom: '2rem' }}>
            <p>Conectado como: <strong>{user.username}</strong></p>
          </div>
        ) : null}

        <nav className="tabs">
          <button 
            className={`tab ${activeTab === 'auth' ? 'active' : ''}`}
            onClick={() => setActiveTab('auth')}
          >
            Acesso
          </button>
          <button 
            className={`tab ${activeTab === 'qrcode' ? 'active' : ''}`}
            disabled={!user}
            onClick={() => setActiveTab('qrcode')}
          >
            QR Code
          </button>
          <button 
            className={`tab ${activeTab === 'barcode' ? 'active' : ''}`}
            disabled={!user}
            onClick={() => setActiveTab('barcode')}
          >
            Barras
          </button>
          <button 
            className={`tab ${activeTab === 'whatsapp' ? 'active' : ''}`}
            disabled={!user}
            onClick={() => setActiveTab('whatsapp')}
          >
            WhatsApp
          </button>
        </nav>
      </div>

      <main className="card">
        {activeTab === 'auth' && (
          <div className="fade-in">
            <h2>Autenticação Local</h2>
            <form onSubmit={handleLogin}>
              <div className="input-group">
                <label>Usuário</label>
                <input 
                  type="text" 
                  value={username} 
                  onChange={(e) => setUsername(e.target.value)} 
                  placeholder="admin"
                />
              </div>
              <div className="input-group">
                <label>Senha</label>
                <input 
                  type="password" 
                  value={password} 
                  onChange={(e) => setPassword(e.target.value)} 
                  placeholder="••••••••"
                />
              </div>
              <button type="submit">Entrar no Sistema</button>
            </form>
          </div>
        )}

        {activeTab === 'qrcode' && (
          <div className="fade-in">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
              <div>
                <h3>Gerar QR Code</h3>
                <div className="input-group">
                  <label>ID do Registro</label>
                  <input 
                    type="number" 
                    value={recordId} 
                    onChange={(e) => setRecordId(e.target.value)} 
                    placeholder="Ex: 123"
                  />
                </div>
                <button onClick={handleGenerateQR}>Gerar Código</button>
                {qrCode && (
                  <div className="qr-display">
                    <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" />
                  </div>
                )}
              </div>
              <div>
                <h3>Ler QR Code</h3>
                <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
                  <p>Clique para upload de QR Code</p>
                  <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileChange} accept="image/*" />
                </div>
                {decodedData && <div className="result-box"><strong>Resultado:</strong><br />{decodedData}</div>}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'barcode' && (
          <div className="fade-in">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
              <div>
                <h3>Gerar Código de Barras</h3>
                <div className="input-group">
                  <label>Conteúdo do Código</label>
                  <input 
                    type="text" 
                    value={barcodeData} 
                    onChange={(e) => setBarcodeData(e.target.value)} 
                    placeholder="Ex: 789123456"
                  />
                </div>
                <button onClick={handleGenerateBarcode}>Gerar Barras</button>
                {barcodeImg && (
                  <div className="qr-display">
                    <img src={`data:image/png;base64,${barcodeImg}`} alt="Barcode" />
                  </div>
                )}
              </div>
              <div>
                <h3>Ler Código de Barras</h3>
                <div className="upload-area" onClick={() => barcodeFileInputRef.current?.click()}>
                  <p>Clique para upload de Código de Barras</p>
                  <input type="file" ref={barcodeFileInputRef} style={{ display: 'none' }} onChange={handleBarcodeFileChange} accept="image/*" />
                </div>
                {decodedBarcode && <div className="result-box"><strong>Resultado:</strong><br />{decodedBarcode}</div>}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'whatsapp' && (
          <div className="fade-in">
            <h2>Enviar WhatsApp</h2>
            <div className="input-group">
              <label>Número do WhatsApp</label>
              <input type="text" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="+55 11 99999-9999" />
            </div>
            <div className="input-group">
              <label>Mensagem</label>
              <input type="text" value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Olá..." />
            </div>
            <button onClick={handleSendMessage}>Enviar Agora</button>
            {sendResult && <div className={`status-badge ${sendResult.success ? 'status-success' : ''}`}>Status: {sendResult.success ? 'Enviado' : 'Falha'}</div>}
          </div>
        )}
      </main>
    </div>
  )
}

export default App
