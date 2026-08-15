WITH SOURCE AS (
    SELECT
        ID,
        CREATED_DATE,
        API_TIMESTAMP,
        JSON
    FROM {{ source('bronze', 'RAW_BUS_POSITIONS') }}
),

LINES AS (
    SELECT
        S.ID,
        S.CREATED_DATE,
        S.API_TIMESTAMP,
        L.LINHA_LETREIRO,
        L.COD_LINHA,
        L.SENTIDO,
        L.DESTINO_I,
        L.DESTINO_II,
        L.VEICULOS
    FROM SOURCE S
    CROSS APPLY openjson(S.JSON, '$.l')
        WITH (
            LINHA_LETREIRO  NVARCHAR(20)  '$.c',
            COD_LINHA       INT           '$.cl',
            SENTIDO         TINYINT       '$.sl',
            DESTINO_I       NVARCHAR(100) '$.lt0',
            DESTINO_II      NVARCHAR(100) '$.lt1',
            VEICULOS        NVARCHAR(MAX) '$.vs' AS JSON
        ) L
),

VEICULOS AS (
    SELECT
        LN.ID,
        LN.CREATED_DATE,
        LN.API_TIMESTAMP,
        LN.LINHA_LETREIRO,
        LN.COD_LINHA,
        LN.SENTIDO,
        LN.DESTINO_I,
        LN.DESTINO_II,
        V.PREFIXO,
        V.ACESSIVEL,
        V.DATA_POSICAO,
        V.LATITUDE,
        V.LONGITUDE
    FROM LINES LN
    CROSS APPLY openjson(LN.VEICULOS, '$')
        WITH (
            PREFIXO       INT            '$.p',
            ACESSIVEL     BIT            '$.a',
            DATA_POSICAO  DATETIME2      '$.ta',
            LATITUDE      DECIMAL(10, 7) '$.py',
            LONGITUDE     DECIMAL(10, 7) '$.px'
        ) V
)

SELECT * FROM VEICULOS