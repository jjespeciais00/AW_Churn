import AgentBox from './AgentBox'

function Dashboard(){
  return(
    <div className="container">
      <h1>AW_Churn</h1>
      <p>
        AI-powered analytics platform
      </p>

      <div className="metrics">
        <div className="card">
          <h3>Total Revenue</h3>
          <p>R$ 0</p>
        </div>
        <div className="card">
          <h3>Total Orders</h3>
          <p>0</p>
        </div>
      </div>

      <div className="table">
        <h2>Products</h2>
        <p>Table placeholder</p>
      </div>

      <AgentBox/>
    </div>
  )
}

export default Dashboard
