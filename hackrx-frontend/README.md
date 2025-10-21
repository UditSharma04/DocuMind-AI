# DocuMind AI - Frontend

**Modern Next.js Frontend for Intelligent Document Queries**

This is the frontend application for DocuMind AI, built with Next.js 15, TypeScript, and Tailwind CSS. It provides a beautiful, responsive interface for document management and AI-powered queries.

## 🚀 Tech Stack

- **Next.js 15**: React framework with Turbopack for fast development
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/ui**: Beautiful, accessible UI components
- **Axios**: HTTP client for API communication
- **Lucide React**: Modern icon library

## 📋 Prerequisites

- Node.js 18+ or npm/yarn/pnpm/bun
- Backend API running on `http://localhost:8000` (see `../llm_retrieval_system/README.md`)

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
# Using npm
npm install

# Using yarn
yarn install

# Using pnpm
pnpm install

# Using bun
bun install
```

### 2. Configure Environment Variables

Create a `.env.local` file in the root directory:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
# Using npm
npm run dev

# Using yarn
yarn dev

# Using pnpm
pnpm dev

# Using bun
bun dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

## 📁 Project Structure

```
hackrx-frontend/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── layout.tsx    # Root layout with metadata
│   │   ├── page.tsx      # Main page component
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   │   ├── ui/          # Shadcn/ui components
│   │   ├── DocumentUpload.tsx      # File upload interface
│   │   ├── DocumentManager.tsx     # Document management
│   │   ├── DocumentSelector.tsx    # Document selection for queries
│   │   ├── QueryInterface.tsx      # Q&A interface
│   │   └── StatusBar.tsx          # System health status
│   └── lib/             # Utility functions
│       └── api.ts       # API client and types
├── public/              # Static assets
├── .env.local          # Environment variables (create this)
├── next.config.ts      # Next.js configuration
├── tailwind.config.ts  # Tailwind CSS configuration
├── tsconfig.json       # TypeScript configuration
└── package.json        # Dependencies and scripts
```

## 🎨 Features

### 📤 Upload Tab
- Drag-and-drop file upload
- Support for PDF, DOCX, DOC, and TXT files
- Real-time upload progress
- Success notifications with file metadata
- Upload statistics display

### 📊 Manage Tab
- View all uploaded documents
- File type badges (PDF, DOCX, TXT)
- Upload timestamps
- Chunk count information
- Delete documents with confirmation
- Refresh functionality
- Empty state handling

### 💬 Query Tab
- Document selector with checkboxes
- "Select All" / "Deselect All" functionality
- Multiple question input
- Real-time query processing
- AI-generated answers with citations
- Query history display
- Loading states and error handling

### 🔧 Additional Features
- Real-time backend health monitoring
- Responsive design for all screen sizes
- Accessible UI components
- Error boundaries and fallbacks
- Optimistic UI updates

## 🌐 Available Scripts

```bash
# Development
npm run dev          # Start development server with Turbopack

# Production
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler check
```

## 🔌 API Integration

The frontend communicates with the backend API through the following endpoints:

### Health Check
- `GET /health` - Check backend status

### Document Management
- `GET /api/v1/documents/` - List all documents
- `POST /api/v1/documents/upload` - Upload a document
- `DELETE /api/v1/documents/{id}` - Delete a document

### Query Processing
- `POST /hackrx/run` - Submit questions and get AI-generated answers
  - Requires Authorization header with Bearer token
  - Body: `{ documents: string[], questions: string[] }`

## 🎨 Customization

### Styling
- Modify `tailwind.config.ts` for theme customization
- Update `src/app/globals.css` for global styles
- Use Tailwind utility classes for component styling

### Components
- Add new components in `src/components/`
- Use Shadcn/ui components from `src/components/ui/`
- Follow TypeScript best practices for type safety

### API Configuration
- Update `src/lib/api.ts` for new endpoints
- Modify API_BASE_URL in `.env.local` for different backends
- Add new API types and interfaces

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
lsof -ti :3000 | xargs kill -9

# Or use a different port
npm run dev -- --port 3001
```

### Module Not Found Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Hydration Errors
The app includes `suppressHydrationWarning={true}` in the body tag to prevent browser extension-related hydration mismatches. This is safe and doesn't affect functionality.

### API Connection Issues
- Ensure backend is running on `http://localhost:8000`
- Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
- Verify CORS is enabled in the backend
- Check browser console for detailed error messages

## 📱 Responsive Design

The UI is fully responsive with breakpoints:
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

All components adapt seamlessly to different screen sizes.

## ♿ Accessibility

- Semantic HTML elements
- ARIA labels and roles
- Keyboard navigation support
- Screen reader friendly
- High contrast mode compatible

## 🚀 Deployment

### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Docker
```bash
# Build image
docker build -t documind-frontend .

# Run container
docker run -p 3000:3000 documind-frontend
```

### Environment Variables for Production
```bash
NEXT_PUBLIC_API_URL=https://your-backend-api.com
```

## 🔄 Updates and Maintenance

- Keep dependencies updated: `npm update`
- Check for security vulnerabilities: `npm audit`
- Update Shadcn/ui components: `npx shadcn@latest add [component]`

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Shadcn/ui Documentation](https://ui.shadcn.com)

---

**Made with ❤️ by Udit Sharma**
