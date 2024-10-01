{
  description = "Peracotta development environment";

  inputs.nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/0.1.*.tar.gz";

  outputs = { self, nixpkgs }:
    let
      supportedSystems =
        [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f:
        nixpkgs.lib.genAttrs supportedSystems
          (system: f { pkgs = import nixpkgs { inherit system; }; });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs;
            [ python39 xcb-util-cursor ]
            ++ (with pkgs.python39Packages; [ pip virtualenv pyqt5 ]);
          shellHook = ''
            echo
            echo "Activated environment"
          '';
          QT_QPA_PLATFORM_PLUGIN_PATH="/nix/store/dw2iadyxy009bidf85fw9hpcq3zyiqdm-qtbase-5.15.12-bin/lib/qt-5.15.12/plugins/platforms";
        };
      });
    };
}
