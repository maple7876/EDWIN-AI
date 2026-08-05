export async function getHardware() {
  const res = await fetch("http://127.0.0.1:8000/hardware");

  if (!res.ok) {
    throw new Error("Failed to detect hardware");
  }

  return await res.json();
}