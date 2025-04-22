# Blog with Hover Animation

A modern blog application built with Vue 3, Vite, and TailwindCSS, featuring smooth hover animations and a clean, organized codebase.

## Project Structure

The project follows a well-organized directory structure:

```
src/
├── api/                  # API services and data fetching
│   ├── index.js          # API exports
│   ├── postApi.js        # Post-related API calls
│   ├── userApi.js        # User-related API calls
│   └── ...
├── assets/               # Static assets
│   ├── css/              # CSS files
│   ├── fonts/            # Font files
│   ├── icons/            # Icon files
│   └── images/           # Image files
├── components/           # Vue components
│   ├── admin/            # Admin-related components
│   ├── blog/             # Blog-related components
│   ├── common/           # Common/shared components
│   ├── layout/           # Layout components (Navbar, Footer, etc.)
│   └── ui/               # UI components (Button, Input, etc.)
├── composables/          # Vue composables
├── constants/            # Constants and configuration
├── data/                 # Mock data
├── hooks/                # Custom hooks
│   ├── index.js          # Hooks exports
│   ├── usePostAnimation.js # Post animation hook
│   └── useTheme.js       # Theme management hook
├── router/               # Vue Router configuration
├── stores/               # State management
├── types/                # TypeScript types
├── utils/                # Utility functions
│   ├── index.js          # Utils exports
│   ├── axios.js          # Axios configuration
│   └── message.js        # Message utility
└── views/                # Vue views/pages
```

## Features

- Modern Vue 3 Composition API
- Vite for fast development and building
- TailwindCSS for styling
- Dark mode support
- Smooth animations with GSAP
- Smooth scrolling with Lenis
- Responsive design
- Well-organized and maintainable code structure

## Getting Started

### Prerequisites

- Node.js (v14+)
- npm or yarn

### Installation

1. Clone the repository
2. Install dependencies:

```bash
npm install
# or
yarn
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Building for Production

```bash
npm run build
# or
yarn build
```

## License

This project is licensed under the MIT License.
