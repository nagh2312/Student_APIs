"use client";

import { Tabs } from "@/components/ui/tabs";
import { CodeBlock } from "@/components/ui/code-block";

export function LanguageExamples({
  curl,
  javascript,
  python,
}: {
  curl: string;
  javascript: string;
  python: string;
}) {
  return (
    <Tabs
      items={[
        {
          id: "curl",
          label: "cURL",
          content: <CodeBlock code={curl} language="bash" />,
        },
        {
          id: "javascript",
          label: "JavaScript",
          content: <CodeBlock code={javascript} language="javascript" />,
        },
        {
          id: "python",
          label: "Python",
          content: <CodeBlock code={python} language="python" />,
        },
      ]}
    />
  );
}
