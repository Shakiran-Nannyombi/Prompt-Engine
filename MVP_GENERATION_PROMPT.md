# Prompt Engine MVP Generation Prompt

## Project Overview
Create a complete MVP (Minimum Viable Product) for **Prompt Engine** - an AI-powered prompt engineering platform with two main agents: a Coaching Agent and a Refiner Agent.

## Core Application Architecture

### Technology Stack
- **Frontend**: Vue 3 + Composition API, Vite, Tailwind CSS 4, Pinia (state management), Vue Router
- **Backend**: FastAPI (Python), PostgreSQL, LangGraph agents
- **AI Integration**: LLM agents for prompt coaching and refinement
- **Styling**: Custom theme system with dark/light mode support

### Custom Theme System
**Light Mode Colors:**
- Primary: `#f60968` (Brand Pink)
- Secondary: `#e8d7ef` (Light Purple) 
- Accent: `#c4a3d2` (Medium Purple)
- Background: `#e6e5fb` (Light Lavender)
- Text: `#1f1e1e` (Dark Gray)

**Dark Mode Colors:**
- Primary: `#f60968` (Brand Pink - consistent)
- Secondary: `#200f27` (Dark Purple)
- Accent: `#4e2d5c` (Medium Dark Purple)
- Background: `#05041a` (Very Dark Blue)
- Text: `#e1e0e0` (Light Gray)

## Application Structure

### 1. Core Views & Routing
```
/ (HomeView) - Landing page with agent selection
/coaching (CoachView) - AI coaching interface
/refiner (RefinerView) - Prompt refinement interface
/login (LoginView) - User authentication
/register (RegisterView) - User registration
/tutorials (TutorialsView) - Video tutorials
/docs (DocsView) - Documentation
```

### 2. Component Architecture

#### Base Components (src/components/base/)
- **BaseButton.vue**: Consistent button with loading states, variants (primary, secondary, outline, ghost)
- **BaseInput.vue**: Form input with validation, error states, clear button
- **BaseCard.vue**: Container with slots for header/body/footer, variants (elevated, outlined, flat)
- **BaseSpinner.vue**: Loading animations with logo integration (PE_logo.svg)
- **BaseModal.vue**: Pop-up dialogs with backdrop, escape key, body scroll lock

#### Layout Components (src/components/layout/)
- **TheHeader.vue**: Navigation with logo, theme toggle, auth state, mobile menu
- **TheFooter.vue**: Footer with links, newsletter signup, social media
- **Sidebar.vue**: Flexible sidebar with collapsible functionality

#### Chat Components (src/components/chat/)
- **ChatInterface.vue**: Main chat wrapper (organism component)
- **ChatMessageList.vue**: Message display with auto-scroll, empty states
- **ChatMessage.vue**: Single message bubble with markdown support
- **ChatInput.vue**: Input with send button, file upload, voice input, shortcuts

#### Feature-Specific Components
- **CoachProgressTracker.vue**: Progress tracking for coaching steps
- **DocumentUpload.vue**: File upload with drag/drop, validation, recent files
- **LoginForm.vue**: Authentication form with validation
- **RegisterForm.vue**: Registration with password strength, terms acceptance
- **VideoCard.vue**: Tutorial video display with metadata, progress tracking
- **VideoPlayer.vue**: Full-featured video player with controls, keyboard shortcuts

### 3. State Management (Pinia Stores)

#### Coaching Store (stores/coaching.js)
```javascript
state: {
  messages: [], // Conversation history
  loading: false,
  error: null,
  currentStep: 'start', // Coaching step tracking
  refinedPrompt: null,
  threadId: null
}
```

#### Refiner Store (stores/refiner.js)
```javascript
state: {
  messages: [], // Conversation history
  loading: false,
  error: null,
  refinedPrompt: null,
  promptCategory: null, // AI-determined category
  frameworkUsed: null, // C.O.R.E, R.A.C.E, C.A.R
  refinementAnalysis: null,
  threadId: null,
  hasDocument: false // Document upload state
}
```

### 4. API Integration (service/api.js)
- **coachingAPI**: `/coaching/chat`, `/coaching/threads/`
- **refinerAPI**: `/refiner/refine_chat`, `/refiner/threads/`
- Response parsing for conversation history, refined prompts, analysis data

## Core Features to Implement

### 1. AI Coaching Agent
**Purpose**: Guide users through structured prompt engineering process

**4-Step Process:**
1. **Task Definition**: Help user define what they want to accomplish
2. **Context Gathering**: Collect background information and requirements
3. **Reference Collection**: Gather examples, resources, constraints
4. **Final Prompt Creation**: Synthesize into optimized prompt

**Features:**
- Progress tracking with visual indicators
- Step-by-step guidance with AI assistance
- Automatic grammar correction
- Final prompt download functionality
- Conversation history preservation

### 2. AI Refiner Agent
**Purpose**: Enhance existing prompts using intelligent frameworks

**Capabilities:**
- **Prompt Categorization**: Automatically classify prompt type (clarity, precision, creative, etc.)
- **Framework Selection**: Choose appropriate framework (C.O.R.E, R.A.C.E, C.A.R)
- **Document Q&A**: RAG-based question answering with uploaded documents
- **Analysis View**: Show reasoning behind refinements
- **Conversation History**: Maintain context across interactions

**Frameworks:**
- **C.O.R.E**: Context, Objective, Requirements, Examples
- **R.A.C.E**: Role, Audience, Context, Expectations  
- **C.A.R**: Context, Action, Result

### 3. User Authentication
- Login/Register forms with validation
- Password strength indicators
- Terms of service acceptance
- Session management
- User profile management

### 4. Tutorial System
- Video card grid layout
- Video player with custom controls
- Progress tracking for watched content
- Bookmark and share functionality
- Category-based organization

## UI/UX Requirements

### Design Principles
- **Mobile-First**: Responsive design for all screen sizes
- **Accessibility**: ARIA labels, keyboard navigation, focus management
- **Performance**: Optimized rendering, lazy loading, smooth animations
- **Consistency**: Unified design system across all components

### Key Interactions
- **Theme Toggle**: Seamless dark/light mode switching
- **Chat Interface**: Real-time messaging with typing indicators
- **File Upload**: Drag & drop with progress indicators
- **Video Playback**: Custom controls with keyboard shortcuts
- **Form Validation**: Real-time feedback with error states

### Animation & Transitions
- Smooth page transitions
- Loading states with branded spinner
- Hover effects and micro-interactions
- Fade-in animations for new content
- Progress bar animations

## Technical Implementation Details

### Component Composition
- Use composition API throughout
- Proper prop validation and TypeScript-like interfaces
- Emit events for parent-child communication
- Expose methods for parent component access

### State Management
- Pinia stores for global state
- Reactive data with proper getters/actions
- Error handling and loading states
- Thread-based conversation management

### API Integration
- Axios for HTTP requests
- Proper error handling and timeouts
- Response parsing and data extraction
- Thread ID management for conversations

### Styling Approach
- Tailwind CSS with custom theme integration
- CSS custom properties for dynamic theming
- Component-scoped styles where needed
- Responsive utility classes

## MVP Success Criteria

### Core Functionality
1. **Working Chat Interfaces**: Both coaching and refiner agents functional
2. **Progress Tracking**: Visual progress indicators for coaching steps
3. **File Upload**: Document upload and processing for refiner
4. **Theme System**: Complete dark/light mode implementation
5. **Responsive Design**: Mobile and desktop compatibility

### User Experience
1. **Intuitive Navigation**: Clear routing and component hierarchy
2. **Error Handling**: Graceful error states and user feedback
3. **Loading States**: Proper loading indicators throughout
4. **Accessibility**: Keyboard navigation and screen reader support
5. **Performance**: Fast loading and smooth interactions

### Technical Quality
1. **Component Architecture**: Reusable, composable components
2. **State Management**: Clean, predictable state updates
3. **API Integration**: Robust error handling and data flow
4. **Code Quality**: Consistent patterns and best practices
5. **Documentation**: Clear component APIs and usage examples

## Implementation Priority

### Phase 1: Core Infrastructure
1. Set up routing and basic layout
2. Implement theme system and base components
3. Create authentication flow
4. Set up state management stores

### Phase 2: Chat Functionality
1. Build chat component system
2. Implement coaching agent interface
3. Create refiner agent interface
4. Add progress tracking

### Phase 3: Advanced Features
1. File upload and document processing
2. Video tutorial system
3. User profile and settings
4. Analytics and usage tracking

### Phase 4: Polish & Optimization
1. Performance optimization
2. Accessibility improvements
3. Error handling refinement
4. User testing and feedback integration

## Expected Deliverables

1. **Complete Vue 3 Application**: All views, components, and routing
2. **Responsive Design**: Mobile and desktop layouts
3. **Theme System**: Dark/light mode with custom colors
4. **Component Library**: Reusable base and feature components
5. **State Management**: Pinia stores for data flow
6. **API Integration**: Backend communication layer
7. **Documentation**: Component usage and API documentation

## Success Metrics

- **Functionality**: All core features working as specified
- **Performance**: Fast loading times and smooth interactions
- **Usability**: Intuitive user experience across devices
- **Accessibility**: WCAG compliance and keyboard navigation
- **Code Quality**: Clean, maintainable, and well-documented code

This MVP should demonstrate the full potential of the Prompt Engine platform while providing a solid foundation for future enhancements and scaling.
