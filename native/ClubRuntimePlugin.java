package live.sahyekfootball.app;

import android.webkit.WebView;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

@CapacitorPlugin(name = "ClubRuntime")
public class ClubRuntimePlugin extends Plugin {
    private String resource(String name) {
        int id = getContext().getResources().getIdentifier(name, "string", getContext().getPackageName());
        return id == 0 ? "" : getContext().getString(id);
    }
    @PluginMethod public void status(PluginCall call) {
        JSObject result = new JSObject();
        String project = resource("project_id");
        String sender = resource("gcm_defaultSenderId");
        result.put("firebaseConfigured", !resource("google_app_id").isEmpty() && !sender.isEmpty() && "football-f4a74".equals(project));
        result.put("firebaseProject", project);
        result.put("senderId", sender);
        android.content.pm.PackageInfo provider = WebView.getCurrentWebViewPackage();
        result.put("webViewVersion", provider == null ? "unavailable" : provider.versionName);
        call.resolve(result);
    }
}