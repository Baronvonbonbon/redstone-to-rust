/* Level 13's door. Installed setuid miner14 so it can read miner14's
 * password, but only prints it when called with the right options. */
#include <stdio.h>
#include <string.h>

static void usage(void) {
    puts("Usage: ./door [OPTIONS]");
    puts("");
    puts("A very old and very fussy mineshaft door.");
    puts("");
    puts("Options:");
    puts("  --help          show this message");
    puts("  --knock N       knock on the door N times (it likes exactly 3)");
    puts("  --say WORD      say a magic word to the door (it likes 'please')");
    puts("");
    puts("The door only opens if you knock the right number of times");
    puts("AND say the right word, in the same command.");
}

int main(int argc, char **argv) {
    int knocks = 0, polite = 0;
    if (argc == 1) {
        puts("The door is locked. It has a sign: 'Try ./door --help'");
        return 1;
    }
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--help")) { usage(); return 0; }
        else if (!strcmp(argv[i], "--knock") && i + 1 < argc) knocks = !strcmp(argv[++i], "3");
        else if (!strcmp(argv[i], "--say") && i + 1 < argc) polite = !strcmp(argv[++i], "please");
        else { printf("The door doesn't understand '%s'. Try ./door --help\n", argv[i]); return 1; }
    }
    if (!knocks) { puts("*knock knock*  ...the door wants a different number of knocks."); return 1; }
    if (!polite) { puts("The door says: 'What's the magic word?'"); return 1; }
    FILE *f = fopen("/etc/mineshaft/pass/miner14", "r");
    if (!f) { puts("The door is stuck. Ask your guide to restart the mineshaft."); return 2; }
    char buf[128] = {0};
    if (!fgets(buf, sizeof buf, f)) buf[0] = 0;
    fclose(f);
    printf("CREEEAK! The door swings open. The password for miner14 is: %s", buf);
    return 0;
}
