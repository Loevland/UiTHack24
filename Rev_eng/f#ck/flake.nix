# This flake was initially generated by fh, the CLI for FlakeHub (version 0.1.9)
{
  description = "UiTHack Fsharp";

  inputs = {
    flake-schemas.url = "https://flakehub.com/f/DeterminateSystems/flake-schemas/*.tar.gz";
    nixpkgs.url = "https://flakehub.com/f/NixOS/nixpkgs/*.tar.gz";
  };

  outputs = { self, flake-schemas, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      schemas = flake-schemas.schemas;

      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {

          packages = with pkgs; [
            nixpkgs-fmt
          ];

          nativeBuildinputs = with pkgs; [
            dotnet-sdk_8
            fsautocomplete
          ];
        };
      });
    };
}
