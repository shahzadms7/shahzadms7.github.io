"""Self-contained SVG architecture views; public patterns, not client topology."""
from pathlib import Path
from html import escape
import base64
import textwrap
ROOT=Path(__file__).parent

def icon(name):
 p=ROOT/'assets/icons'/f'{name}.svg'
 if p.exists():return 'data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()
 p=ROOT/'assets/icons'/f'{name}.png'
 return 'data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode() if p.exists() else ''

def platform_strip():
 names=[('azure','Microsoft Azure'),('aws','Amazon Web Services'),('gcp','Google Cloud'),('microsoft','Microsoft 365'),('k8s','Kubernetes'),('terraform','Terraform'),('docker','Docker'),('python','Python'),('foundry','Microsoft Foundry'),('bedrock','Amazon Bedrock'),('vertex','Vertex AI'),('ai-search','Azure AI Search'),('sentinel','Microsoft Sentinel'),('azure-monitor','Azure Monitor'),('bigquery','BigQuery'),('databricks','Databricks')]
 return '<div class="platform-wall" aria-label="Selected technology platforms">'+''.join(f'<div><img src="assets/icons/{i}.svg" alt="" width="34" height="34"><span>{n}</span></div>' for i,n in names)+'</div>'

def svg(title, subtitle, nodes, edges, bands=()):
 out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 650" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(subtitle)}. Arrows show flow; dashed lines show feedback or cross-cutting controls.</desc><defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#34717e"/></marker><style>text{{font-family:Arial,sans-serif}}.title{{font-size:24px;font-weight:700;fill:#12283e}}.sub{{font-size:14px;fill:#41546a}}.label{{font-size:17px;font-weight:700;fill:#12283e}}.detail{{font-size:13px;fill:#41546a}}.edge{{fill:none;stroke:#34717e;stroke-width:2.5;marker-end:url(#arrow)}}.lane{{font-size:12px;font-weight:700;letter-spacing:1px;fill:#34576f}}</style></defs><rect width="1040" height="650" rx="18" fill="#f5f8fc"/><text x="30" y="40" class="title">{escape(title)}</text><text x="30" y="67" class="sub">{escape(subtitle)}</text>']
 for y,h,label in bands:
  out.append(f'<rect x="20" y="{y}" width="1000" height="{h}" rx="12" fill="#e6eef6" stroke="#bacbdc" stroke-dasharray="6 5"/><text x="36" y="{y+22}" class="lane">{escape(label)}</text>')
 for a,b,mode in edges:
  ax,ay=nodes[a][:2];bx,by=nodes[b][:2]
  if ay==by:
   x1,x2=(ax+270,bx) if bx>ax else (ax,bx+270);path=f'M{x1} {ay+45} H{x2}'
  elif ax==bx:path=f'M{ax+135} {ay+90 if by>ay else ay} V{by if by>ay else by+90}'
  else:
   x1,y1=ax+135,(ay+90 if by>ay else ay);x2,y2=bx+135,(by if by>ay else by+90)
   path=f'M{x1} {y1} V{(y1+y2)/2} H{x2} V{y2}'
  out.append(f'<path d="{path}" class="edge"'+(' stroke-dasharray="6 4"' if mode else '')+'/>')
 for x,y,label,detail,im in nodes:
  out.append(f'<rect x="{x}" y="{y}" width="270" height="90" rx="10" fill="white" stroke="#a7bed2" stroke-width="1.5"/><rect x="{x}" y="{y}" width="5" height="90" rx="2" fill="#087f8c"/>')
  if im and icon(im):out.append(f'<image href="{icon(im)}" x="{x+14}" y="{y+16}" width="32" height="32"/>')
  tx=x+(56 if im and icon(im) else 16)
  available=x+254-tx
  label_size=min(17,available/max(1,len(label)*0.55))
  out.append(f'<text x="{tx}" y="{y+32}" class="label" style="font-size:{label_size:.1f}px">{escape(label)}</text>')
  for j,line in enumerate([part for line in detail.split('|') for part in textwrap.wrap(line,width=38)]):out.append(f'<text x="{x+16}" y="{y+58+j*17}" class="detail">{escape(line)}</text>')
 out.append('<text x="30" y="627" class="sub">Representative pattern • Services selected by workload • Client topology withheld</text></svg>')
 return ''.join(out)

# All views share generous spacing and explicit service boundaries.
VIEWS=[
('01','Microsoft / Azure','Connect business operations, trusted data and controlled AI.',
 [('Users & operations','Stores · staff · business applications',''),('Entra ID & access','SSO · MFA · RBAC · PIM','microsoft'),('Azure application tier','Front Door / WAF · AKS / APIs','azure'),('Data & integration','Databricks · SQL · event pipelines','databricks'),('Search & knowledge','Azure AI Search · permission filters','ai-search'),('Microsoft Foundry','Models · agents · scoped tools','foundry'),('Security operations','Defender · Sentinel · Key Vault','microsoft'),('Service operations','Azure Monitor · SLOs · cost','azure-monitor'),('Recovery & approval','Backup · restore · human review','')],
 [(0,1,0),(1,2,0),(2,5,0),(3,4,0),(4,5,0),(0,3,0),(6,3,1),(7,4,1),(8,5,1)],
 'Application requests pass through identity and the application tier. Governed data feeds search and agents. Security, telemetry and recovery apply across the environment.'),
('02','AWS / AI & SaaS','Separate product delivery, data and AI within a governed AWS estate.',
 [('Customers & tenants','Web / mobile · tenant-aware access',''),('Edge & identity','CloudFront · WAF · Cognito','aws'),('Product services','API Gateway · Lambda / EKS','lambda'),('Persistent data','S3 · Aurora / RDS · encryption','s3'),('Amazon Bedrock','Knowledge Bases · agents · models','bedrock'),('Business actions','Scoped APIs · approval · audit',''),('Cloud governance','Organizations · IAM · KMS','aws'),('Observe & evaluate','CloudWatch · traces · AI evaluation','cloudwatch'),('Continuity & cost','Recovery · budgets · usage limits','')],
 [(0,1,0),(1,2,0),(2,5,0),(2,4,0),(3,4,0),(4,5,0),(6,3,1),(7,4,1),(8,5,1)],
 'Authenticated product requests use application services. Bedrock retrieves permitted knowledge and calls scoped business tools. Observability, account controls and recovery span every layer.'),
('03','MSP / CSP / MSSP','Repeatable customer delivery with isolated tenants and shared operations.',
 [('Customer discovery','Scope · SLA / OLA · data boundaries',''),('Landing-zone standards','Identity · network · policy · billing','terraform'),('Delivery pipeline','IaC · review · migration waves','githubactions'),('Azure / Microsoft','Customer-specific subscription','azure'),('AWS','Customer-specific account','aws'),('Google / IBM / Oracle','Customer-specific cloud tenancy','gcp'),('Service desk & SOC','L1 / L2 / L3 · incidents · escalation',''),('Recovery & capacity','Backups · DR · scaling · FinOps',''),('Customer improvement','Reporting · review · roadmap','')],
 [(0,1,0),(1,2,0),(1,3,0),(1,4,0),(2,5,0),(3,6,0),(4,7,0),(5,8,0),(6,7,1),(7,8,1)],
 'Discovery defines the service contract and customer boundary. Reusable standards feed separately isolated cloud environments. Support, security, recovery and reporting complete the operating model.'),
('04','Open-source / SaaS product','Deliver a complete user journey with tenant-aware services.',
 [('Users & edge','Browser · CDN · TLS · rate limits',''),('Identity & tenancy','Authentication · RBAC · isolation',''),('Application / APIs','Python · Django / FastAPI','python'),('Background work','Redis · queues · scheduled jobs',''),('Data foundation','PostgreSQL · pgvector · documents',''),('AI orchestration','RAG · model routing · evaluation','python'),('Build & release','GitHub · containers · migrations','docker'),('Operate & recover','Logs · metrics · backup · restore',''),('Learn & improve','User feedback · backlog · releases','')],
 [(0,1,0),(1,2,0),(2,5,0),(2,4,0),(3,4,0),(4,5,0),(6,3,1),(7,4,1),(8,5,1)],
 'Tenant-aware application access protects data and retrieval. Background jobs handle longer tasks. Versioned releases, restore procedures and feedback support the product lifecycle; this is not a claim of all roadmap features being live.'),
('05','ISP / datacentre / hybrid','Availability depends on the entire physical-to-application chain.',
 [('Facility foundations','Rack · power · cooling · cabling',''),('Carrier & network','BGP · routing · firewalls · DNS',''),('Compute & storage','Servers · SAN / NAS · redundancy',''),('Virtual platforms','VMware · Hyper-V · private cloud',''),('Hosted services','Identity · mail · web · databases',''),('Customer access','Provisioning · isolation · service desk',''),('Hybrid extension','Private links · VPN · cloud migration','azure'),('Operations / NOC','Monitoring · capacity · incidents',''),('Recovery site','Replication · restore · failover','')],
 [(0,1,0),(1,2,0),(2,5,0),(2,3,0),(3,4,0),(4,5,0),(3,6,0),(4,7,0),(5,8,0),(6,7,1),(7,8,1)],
 'Facilities and carrier networks support compute and storage. Virtual platforms host customer services. Hybrid connectivity, monitoring and tested recovery address failures across layers.'),
('06','Microsoft 365 / migration','Move identity, mail and collaboration with reconciliation and rollback.',
 [('Source inventory','AD · Exchange · files · permissions','microsoft'),('Migration design','Identity mapping · retention · waves',''),('Coexistence & pilot','Directory sync · test users · checks','microsoft'),('Business validation','Access · mail flow · content checks',''),('Migration waves','Exchange Online · SharePoint · Teams','microsoft'),('Cutover decision','Reconcile · business approval',''),('Rollback path','Restore access · source continuity',''),('Service transition','Hypercare · training · runbooks',''),('Target governance','Entra ID · Purview · audit · support','microsoft')],
 [(0,1,0),(1,2,0),(2,5,0),(3,4,0),(4,5,0),(5,8,0),(5,6,1),(6,7,1),(7,8,0)],
 'Inventory and pilot precede staged moves. Business checks and reconciliation gate cutover. Rollback remains available until acceptance, followed by hypercare and operational ownership.'),
('07','Google Cloud / AI reference','A provider-specific reference for governed retrieval and AI services.',
 [('Users & applications','Business question · authenticated user',''),('API & runtime','Apigee / API gateway · Cloud Run','gcp'),('Vertex AI / agents','Model serving · agent orchestration','vertex'),('Source data','Cloud Storage · BigQuery','bigquery'),('Retrieval & grounding','Index · access filters · context','gcp'),('Response & tools','Citations · approvals · scoped actions',''),('Identity & security','IAM · KMS · policy · secrets','gcp'),('Quality & operations','Evaluation · logs · monitoring','gcp'),('Governance & spend','Audit · budgets · lifecycle controls','')],
 [(0,1,0),(1,2,0),(2,5,0),(3,4,0),(4,2,0),(6,3,1),(7,4,1),(8,5,1)],
 'Reference pattern for discussion, not a separate claimed client deployment. Governed retrieval supplies context to AI services; tools, output evaluation and access controls limit the workflow.')]

from architecture_expansion import EXTRA_VIEWS
VIEWS.extend(EXTRA_VIEWS)

def architecture_section():
 out=['<section class="content architecture-section" id="architecture"><div class="wrap"><div class="section-head"><div><p class="eyebrow">Architecture / See how the systems connect</p><h2>From the big picture<br>to the working parts.</h2></div><p>Connected, presentation-style views for business and technical conversations. Open a view to explore it, or download its scalable diagram.</p></div><p class="diagram-disclaimer">Public reference patterns based on the experience catalog. These explain design choices, not confidential as-built client systems. Solid arrows: flow or dependency. Dashed arrows: controls, feedback or contingency.</p>']
 out.append('<label for="architecture-search" class="sr-only">Search architecture views</label><input class="architecture-search" id="architecture-search" type="search" placeholder="Find an architecture: Linux, licensing, recovery, Oracle, medallion…"><div class="architecture-list">'+''.join(f'<a href="#architecture-{i}">{escape(title)}</a>' for i,title,*_ in VIEWS)+'</div>')
 d=ROOT/'assets/diagrams';d.mkdir(exist_ok=True)
 for i,title,sub,items,edges,desc in VIEWS:
  nodes=[(45+(j%3)*340,135+(j//3)*175,*n) for j,n in enumerate(items)]
  content=svg(title,sub,nodes,edges,[(100,135,'FOUNDATION / INPUTS'),(275,135,'SERVICES / WORKFLOW'),(450,135,'CONTROLS / OPERATIONS')])
  (d/f'architecture-{i}.svg').write_text(content)
  out.append(f'<details class="architecture-view" id="architecture-{i}" {"open" if i=="01" else ""}><summary><span><small>ARCHITECTURE {i}</small>{escape(title)}</span><span class="view-hint">Explore diagram</span></summary><div class="architecture-body"><p>{escape(desc)}</p><figure><img src="assets/diagrams/architecture-{i}.svg" width="1040" height="650" loading="lazy" alt="{escape(desc)}"></figure><div class="diagram-actions"><a class="btn" href="assets/diagrams/architecture-{i}.svg" target="_blank" rel="noopener">Open full size ↗</a><a class="btn" href="assets/diagrams/architecture-{i}.svg" download>Download SVG ↓</a></div></div></details>')
 out.append('<p class="note">Product names remain visible beside platform marks. Brand marks are not certifications or endorsements. <a href="ICON_SOURCES.md">Icon sources and attribution</a>.</p></div></section>')
 return ''.join(out)

def delivery_diagram():
 stages=[('Discovery','Needs · current state · stakeholders'),('Scope & SOW','Deliverables · costs · acceptance'),('Architecture','Options · threat model · decisions'),('Prototype / POC','Prove feasibility · reduce uncertainty'),('MVP','Working end-to-end user journey'),('Pilot & acceptance','User validation · security · recovery'),('Production release','Cutover · rollback · monitoring'),('Operate & hand over','SOP · runbooks · ownership · training'),('Improve','Outcomes · cost · feedback · roadmap')]
 # Serpentine visual makes every dependency explicit without a long thin row.
 positions=[(45,135),(385,135),(725,135),(725,310),(385,310),(45,310),(45,485),(385,485),(725,485)]
 nodes=[(*p,t,d,'') for p,(t,d) in zip(positions,stages)]
 content=svg('The delivery lifecycle','Business decisions, engineering evidence and operational ownership at each stage.',nodes,[(i,i+1,0) for i in range(8)])
 path=ROOT/'assets/diagrams';path.mkdir(exist_ok=True);(path/'delivery-lifecycle.svg').write_text(content)
 return '<figure class="lifecycle"><img src="assets/diagrams/delivery-lifecycle.svg" width="1040" height="650" loading="lazy" alt="Discovery to scope, architecture, prototype, MVP, pilot acceptance, production, handover and improvement."><figcaption>Each transition requires agreed evidence. Unmet criteria return the work to the relevant stage before release.</figcaption><a class="btn light" href="assets/diagrams/delivery-lifecycle.svg" target="_blank" rel="noopener">Open lifecycle full size ↗</a></figure>'
