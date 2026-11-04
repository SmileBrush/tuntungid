import "./globals.css";
import { Inter, Montserrat } from "next/font/google";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter", display: "swap" });
const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["600", "700"],
  variable: "--font-montserrat",
  display: "swap"
});

export const metadata = {
  title: "Tuntung.id | Gawi Manuntung, Supaya Untung",
  description: "Jasa pembuatan aplikasi dan web app kustom, lengkap dengan dashboard untuk memantau proyek Anda."
};

export default function RootLayout({ children }) {
  return (
    <html lang="id" className={`${inter.variable} ${montserrat.variable}`}>
      <body className="bg-ground text-ink selection:bg-brand selection:text-white">{children}</body>
    </html>
  );
}
