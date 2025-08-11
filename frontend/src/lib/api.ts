export const api = {
  async get(path:string){
    const res = await fetch(`/api${path}`,{ headers: {'x-api-key': localStorage.getItem('apiKey')||'change-me'} });
    return res.json();
  },
  async post(path:string, body:any){
    const res = await fetch(`/api${path}`,{ method:'POST', headers:{'Content-Type':'application/json','x-api-key':localStorage.getItem('apiKey')||'change-me'}, body:JSON.stringify(body) });
    return res.json();
  }
};
