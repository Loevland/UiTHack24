open System

[<EntryPoint>]
let main args =
    match args.Length with
    | x when x < 1 ->
            Console.WriteLine("Expected at least one argument, got %i.", args.Length)
    | _ ->
        let secret = args |> Array.head
        let flag = 
            "lano!tkc@f".ToCharArray()
            |> Seq.map (fun c -> char (int c + 1))
            |> Seq.map (fun c -> char (int c - 1))
            |> Array.ofSeq
            |> Array.rev
            |> String
        
        if secret = "D2005S" then
           Console.WriteLine("TD{{%s}", flag)
    0
    
