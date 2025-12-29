Please generate a React TypeScript component with Tailwind CSS from the Figma page [PAGE_NAME] in [FIGMA_URL].

IMPORTANT Requirements:

1. Variables Mapping:
   - Map Figma Variables to standard Tailwind classes
   - Use `bg-slate-50` instead of `bg-[var(--slate-50)]`
   - Use `text-sm` instead of `text-[length:var(--size-sm)]`
2. Semantic HTML:
   - Use semantic elements (`header`, `nav`, `main`, `aside`, `footer`)
   - Use <button> for interactive elements
   - Use <a> for links
3. Interactive Elements:
   - Add hover states (hover:text-blue-600)
   - Add transitions (transition-colors)
   - Add focus states where appropriate
4. Code Quality:
   - Use TypeScript interfaces for props and data
   - Use data-driven approach with .map() for repeated elements
   - Next.js Image/Link components where applicable
   - Clean, production-ready code

Use @figma-mcp-server to access the design.
