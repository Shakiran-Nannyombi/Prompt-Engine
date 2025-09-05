# Prompt Engine Frontend

A modern Vue.js frontend application for the Prompt Engine platform, featuring AI-powered prompt coaching and refinement tools with a beautiful, customizable theme system.

## Features

- **AI Prompt Coaching**: Interactive chat interface for prompt improvement guidance
- **Prompt Refinement**: Advanced prompt optimization with category-based frameworks
- **Custom Theme System**: Beautiful light/dark mode with brand-specific colors
- **Component Library**: Reusable base components built with Tailwind CSS
- **Responsive Design**: Mobile-first approach with modern UI/UX
- **State Management**: Pinia for efficient state management
- **Routing**: Vue Router for seamless navigation

## Project Structure

``` bash
frontend/
├── public/
│   └── PE_logo.svg                 # Brand logo for animations
├── src/
│   ├── assets/
│   │   ├── images/                 # Logo assets (SVG, PNG)
│   │   └── styles/
│   ├── components/
│   │   ├── base/                   # Base component library    
│   │   ├── auth/                   # Authentication components
│   │   ├── chat/                   # Chat interface components
│   │   ├── icons/                  # Icon components
│   │   └── layout/                 # Layout components
│   ├── router/                     # Vue Router configuration
│   ├── service/                    # API service layer
│   ├── stores/                     # Pinia state management
│   ├── views/                      # Page components
│   │   ├── HomeView.vue
│   │   ├── CoachView.vue
│   │   ├── RefinerView.vue
│   │   ├── LoginView.vue
│   │   ├── RegisterView.vue
│   │   ├── DocsView.vue
│   │   └── TutorialsView.vue
│   ├── App.vue                     # Root component
│   └── main.js                     # Application entry point
├── tailwind.config.js              # Tailwind CSS configuration
├── vite.config.js                  # Vite build configuration
└── package.json                    # Dependencies and scripts
```

## Technology Stack

- **Vue 3**: Progressive JavaScript framework with Composition API
- **Vite**: Fast build tool and development server
- **Tailwind CSS 4**: Utility-first CSS framework with custom theme
- **Vue Router**: Official router for Vue.js applications
- **Pinia**: Modern state management for Vue applications
- **Axios**: HTTP client for API communication
- **PostCSS**: CSS post-processor with Autoprefixer

## 📄 License

This project is part of the Prompt Engine platform. See the main project LICENSE file for details.

## Contributing

1. Follow the established component architecture
2. Use the base components as building blocks
3. Maintain theme consistency
4. Write accessible, semantic HTML
5. Test across different screen sizes and themes

---

**Built with ❤️ using Vue 3, Tailwind CSS, and modern web technologies.**
