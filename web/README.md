
# RoutR_MauraDr Web :globe_with_meridians:  

Welcome to the **RoutR_MauraDr Web** subproject! This repository houses the web interface portion of the larger RoutR_MauraDr ecosystem. This front-end aims to provide visualization, configuration, and control of various routing, caching, and distributed networking functionalities in a user-friendly manner[^1](https://github.com/elithaxxor/RoutR_MauraDr/tree/main_pi/web.git).

---

## :star: About  
RoutR_MauraDr Web is designed to make life easier for developers and operations teams by offering a streamlined approach to interacting with back-end routing services. Through this interface, users can revise routing configurations, monitor traffic, and manage distributed caches all in one place.

Key highlights:  
- **Modular Architecture**: Built to integrate seamlessly with the core RoutR_MauraDr services, ensuring easy customization and extensibility.  
- **User-Friendly UI**: Clear layouts, helpful tooltips, and interactive dashboards to keep you productive.  
- **Scalable**: Perfect for local dev environments or large-scale cluster deployments.

---

to start: 
```bash
  celery -A src.tasks.scan_tasks.celery worker --loglevel=info
```


## :sparkles: Features  
1. **Real-time Monitoring** :eyes:  
   Get immediate insights into network traffic, node status, and usage statistics.  

2. **Interactive Configuration** :wrench:  
   Easily adjust routing rules, DNS entries, or caching policies without editing complex config files.  

3. **Analytics & Reporting** :bar_chart:  
   Generate visual reports on traffic distribution, latency trends, and system health over time.

4. **Responsive Design** :iphone:  
   Access and manage routes from any device, ensuring quick changes on the go.

---

## :rocket: Getting Started  

### Prerequisites  
1. **Node.js** (v12+ recommended)  
2. **npm** or **yarn**  
3. **Git** (for cloning the repository)

### Installation  
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/elithaxxor/RoutR_MauraDr.git
   ```  
   Make sure to navigate specifically to the `web` folder if you have cloned the full monorepo.  
   ```bash
   cd RoutR_MauraDr/web
   ```

2. **Install Dependencies**  
   ```bash
   npm install
   ```
   or  
   ```bash
   yarn install
   ```

### Running the Application  
1. **Development Mode**  
   ```bash
   npm run dev
   ```
   This will spin up a local development server (commonly at `http://localhost:3000`) with hot-reloading.  

2. **Production Build**  
   ```bash
   npm run build
   npm start
   ```
   Builds a fully optimized bundle and starts the web server for production.

---

## :gear: Project Structure  
Below is an overview of the typical directory layout for RoutR_MauraDr Web:

```
web
├── public
│   └── ...
├── src
│   ├── components
│   ├── pages
│   ├── services
│   └── ...
├── package.json
└── README.md
```

- **public/**: Houses static assets, like images or fonts.  
- **src/**: Contains main source code, including React components, pages, and service utilities.  

---

