package live.sahyekfootball.app;

import android.os.Bundle;
import android.graphics.Color;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebResourceRequest;
import android.net.Uri;
import android.content.Intent;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowCompat;
import com.getcapacitor.BridgeActivity;
import com.getcapacitor.BridgeWebViewClient;

public class MainActivity extends BridgeActivity {
    @Override public void onCreate(Bundle savedInstanceState) {
        registerPlugin(ClubRuntimePlugin.class);
        super.onCreate(savedInstanceState);
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView()).setAppearanceLightStatusBars(false);
        WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView()).setAppearanceLightNavigationBars(false);
        getWindow().setStatusBarColor(getColor(live.sahyekfootball.app.R.color.club_navy));
        getWindow().setNavigationBarColor(getColor(live.sahyekfootball.app.R.color.club_navy));
        View root = findViewById(android.R.id.content);
        root.setBackgroundColor(getColor(live.sahyekfootball.app.R.color.club_navy));
        getBridge().getWebView().setBackgroundColor(getColor(live.sahyekfootball.app.R.color.club_navy));
        getBridge().getWebView().getSettings().setCacheMode(android.webkit.WebSettings.LOAD_DEFAULT);
        ViewCompat.setOnApplyWindowInsetsListener(root, (view, insets) -> {
            androidx.core.graphics.Insets bars = insets.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
            view.setPadding(bars.left, bars.top, bars.right, bars.bottom);
            return WindowInsetsCompat.CONSUMED;
        });
        getBridge().getWebView().setWebViewClient(new BridgeWebViewClient(getBridge()) {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                if (!request.isForMainFrame()) return super.shouldOverrideUrlLoading(view, request);
                Uri uri = request.getUrl();
                if ("https".equals(uri.getScheme()) && "www.sahyekfootball.live".equals(uri.getHost())) {
                    view.loadUrl(uri.buildUpon().authority("sahyekfootball.live").build().toString());
                    return true;
                }
                if ("https".equals(uri.getScheme()) && ("sahyekfootball.live".equals(uri.getHost()) || "localhost".equals(uri.getHost()))) return false;
                if ("https".equals(uri.getScheme()) || "mailto".equals(uri.getScheme()) || "tel".equals(uri.getScheme())) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, uri)); } catch (Exception ignored) {}
                }
                return true;
            }
        });
    }
}
