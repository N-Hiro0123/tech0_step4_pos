"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const hashPassword = async (password: string): Promise<string> => {
    // パスワードをUint8Arrayにエンコード
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    // SHA-256でハッシュ化
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    // ハッシュを16進数文字列に変換
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
    return hashHex;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    const hashedPassword = await hashPassword(password);

    try {
      const response = await fetch(process.env.NEXT_PUBLIC_API_ENDPOINT + `/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_name: username, user_password: hashedPassword }),
      });

      if (response.status === 200) {
        const data = await response.json();
        localStorage.setItem("token", data["access_token"]); // JWTをローカルストレージに保存
        router.push("/purchase"); // ダッシュボードページへリダイレクト
      } else {
        alert("ログインに失敗しました");
      }
    } catch (error) {
      console.error("ログイン時にエラーが発生しました", error);
      alert("ログインに失敗しました");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200">
      <div className="card w-full max-w-sm shadow-2xl bg-base-100">
        <div className="card-body">
          <h2 className="text-2xl font-bold text-center mb-4">ログイン画面</h2>
          <form onSubmit={handleLogin} className="form-control">
            <div className="form-control mb-4">
              <label className="label">
                <span className="label-text">Username</span>
              </label>
              <input
                type="text"
                placeholder="Username"
                className="input input-bordered"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="form-control mb-4">
              <label className="label">
                <span className="label-text">Password</span>
              </label>
              <input
                type="password"
                placeholder="Password"
                className="input input-bordered"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="form-control mt-6">
              <button type="submit" className="btn btn-primary">
                ログイン
              </button>
            </div>
          </form>
          <div className="mt-4 text-center">
            <p>アカウントをお持ちでないですか？</p>
            <button className="btn btn-link" onClick={() => router.push("/register")}>
              ユーザー登録ページへ
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
