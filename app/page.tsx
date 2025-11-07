export default function Home() {
  return (
    <main style={{padding: 24, fontFamily: 'sans-serif'}}>
      <h1>PerplexiPlay ? Agent Playground</h1>
      <p>
        This is the web landing page for PerplexiPlay deployed on Vercel.
      </p>
      <ul>
        <li>Backend (FastAPI) runs via Docker Compose locally.</li>
        <li>Streamlit UI available locally for rich interaction.</li>
      </ul>
      <p>
        Visit the project README for setup instructions or run the Docker Compose stack.
      </p>
    </main>
  )
}
