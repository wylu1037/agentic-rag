import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
  // Raycast uses OpenType features — load all weights needed
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Agentic RAG",
  description: "基于检索增强生成的智能知识问答系统",
  icons: { icon: "/favicon.ico" },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="zh-CN" className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
